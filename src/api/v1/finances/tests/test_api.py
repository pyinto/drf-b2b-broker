from decimal import Decimal

from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase, APITransactionTestCase
from django.urls.base import reverse

from api.v1.finances.views import WalletViewSet, TransactionViewSet
from models.finances.models import Wallet, Transaction
from models.finances.tests.factories import WalletFactory, TransactionFactory, TransactionNoSignalsFactory
from django.test.utils import CaptureQueriesContext
from django.db import connection
from logging import getLogger

logger = getLogger(__name__)


class WalletAPIIntegrationTestCase(APITransactionTestCase):
    view_cls = WalletViewSet
    serializer_cls = view_cls.serializer_class
    url_list = "api:v1:finances:wallet-list"

    def setUp(self):
        self.maxDiff = None

        self.factory = APIRequestFactory()
        self.view_list = self.view_cls.as_view({"get": "list"})
        self.view_retrieve = self.view_cls.as_view({"get": "retrieve"})

    def test__list__schema(self):
        wallet = WalletFactory(balance=Decimal("9.000000000000000999"))
        expected_data = [
            {
                "attributes": {
                    "balance": f"{wallet.balance}",
                    "label": f"{wallet.label}",
                },
                "id": f"{wallet.id}",
                "type": f"{Wallet.__name__}",
            }
        ]

        url = reverse(self.url_list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()["data"]
        self.assertListEqual(expected_data, actual_data)

    def test__list__filters(self):
        wallet0 = WalletFactory(balance=Decimal("0.0"), label="0")
        wallet1 = WalletFactory(balance=Decimal("1.0"), label="1")
        wallet2 = WalletFactory(balance=Decimal("2.0"), label="2")
        wallet3 = WalletFactory(balance=Decimal("3.0"), label="3")
        wallet4 = WalletFactory(balance=Decimal("4.0"), label="test-4")

        test_cases = (
            # # id:
            (
                reverse(self.url_list, query={"filter[id]": wallet3.id}),
                [wallet3],
            ),
            (
                reverse(self.url_list, query={"filter[id.in]": f"{wallet3.id}, {wallet1.id}"}),
                [wallet1, wallet3],
            ),
            # # label:
            (
                reverse(self.url_list, query={"filter[label]": wallet2.label}),
                [wallet2],
            ),
            (
                reverse(self.url_list, query={"filter[label.icontains]": "test"}),
                [wallet4],
            ),
            # # balance:
            (
                reverse(self.url_list, query={"filter[balance]": f"{wallet2.balance}"}),
                [wallet2],
            ),
            (
                reverse(self.url_list, query={"filter[balance.range]": f"{wallet2.balance}, {wallet3.balance}"}),
                [wallet2, wallet3],
            ),
            (
                reverse(self.url_list, query={"filter[balance.lt]": str(wallet2.balance)}),
                [wallet0, wallet1],
            ),
            (
                reverse(self.url_list, query={"filter[balance.lte]": str(wallet2.balance)}),
                [wallet0, wallet1, wallet2],
            ),
            (
                reverse(self.url_list, query={"filter[balance.gt]": str(wallet2.balance)}),
                [wallet3, wallet4],
            ),
            (
                reverse(self.url_list, query={"filter[balance.gte]": str(wallet2.balance)}),
                [wallet2, wallet3, wallet4],
            ),
            # # sorting:
            (
                reverse(self.url_list, query={"sort": "-balance"}),
                [wallet4, wallet3, wallet2, wallet1, wallet0],
            ),
            (
                reverse(self.url_list, query={"sort": "balance"}),
                [wallet0, wallet1, wallet2, wallet3, wallet4],
            ),
        )

        for url, expected in test_cases:
            with self.subTest(msg=f"Testing {url}"):
                request = self.factory.get(url)
                response = self.view_list(request)
                self.assertEqual(response.status_code, 200, response.data)
                expected_data = self.view_cls.serializer_class(expected, many=True).data
                self.assertListEqual(expected_data, response.data["results"])


class TransactionAPIIntegrationTestCase(APITransactionTestCase):
    view_cls = TransactionViewSet
    serializer_cls = view_cls.serializer_class
    url_list = "api:v1:finances:transaction-list"

    def setUp(self):
        self.maxDiff = None

        self.factory = APIRequestFactory()
        self.view_list = self.view_cls.as_view({"get": "list"})
        self.view_retrieve = self.view_cls.as_view({"get": "retrieve"})

    def test__list__schema(self):
        transaction = TransactionFactory(amount=Decimal("9.000000000000000999"))
        expected_data = [
            {
                "id": f"{transaction.id}",
                "type": f"{Transaction.__name__}",
                "attributes": {
                    "amount": f"{transaction.amount}",
                    "txid": f"{transaction.txid}",
                },
                "relationships": {
                    "wallet": {
                        "data": {
                            "id": f"{transaction.wallet_id}",
                            "type": f"{Wallet.__name__}",
                        },
                    },
                },
            }
        ]

        url = reverse(self.url_list)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()["data"]
        self.assertListEqual(expected_data, actual_data)

    def test__list__filters(self):
        w1 = WalletFactory(balance=Decimal("1.0"), label="1")
        w2 = WalletFactory(balance=Decimal("2.0"), label="2")
        w3 = WalletFactory(balance=Decimal("3.0"), label="test-3")

        w1_tx_1 = TransactionFactory(amount=Decimal("1.0"), wallet=w1, txid="w1_tx_1")
        w1_tx_2 = TransactionFactory(amount=Decimal("2.0"), wallet=w1, txid="w1_tx_2")

        w2_tx_1 = TransactionFactory(amount=Decimal("1.0"), wallet=w2, txid="w2_tx_1")
        w2_tx_2 = TransactionFactory(amount=Decimal("2.0"), wallet=w2, txid="w2_tx_2")

        w3_tx_2 = TransactionFactory(amount=Decimal("2.0"), wallet=w3, txid="w3_tx_2")
        w3_tx_3 = TransactionFactory(amount=Decimal("3.0"), wallet=w3, txid="w3_tx_3")

        test_cases = (
            (
                reverse(self.url_list, query=""),  # default query
                [w3_tx_3, w3_tx_2, w2_tx_2, w2_tx_1, w1_tx_2, w1_tx_1],
            ),
            # # id:
            (
                reverse(self.url_list, query={"filter[id]": f"{w1_tx_2.id}"}),
                [w1_tx_2],
            ),
            (
                reverse(self.url_list, query={"filter[id.in]": f"{w1_tx_2.id}, {w3_tx_3.id}"}),
                [w3_tx_3, w1_tx_2],
            ),
            # # txid:
            (
                reverse(self.url_list, query={"filter[txid]": f"{w3_tx_3.txid}"}),
                [w3_tx_3],
            ),
            (
                reverse(self.url_list, query={"filter[txid.icontains]": "w2"}),
                [w2_tx_2, w2_tx_1],
            ),
            (
                reverse(self.url_list, query={"filter[txid.in]": f"{w1_tx_2.txid}, {w3_tx_3.txid}"}),
                [w3_tx_3, w1_tx_2],
            ),
            # # amount:
            (
                reverse(self.url_list, query={"filter[amount]": f"{w1_tx_1.amount}"}),
                [w2_tx_1, w1_tx_1],
            ),
            (
                reverse(self.url_list, query={"filter[amount.range]": f"{w3_tx_2.amount}, {w3_tx_3.amount}"}),
                [w3_tx_3, w3_tx_2, w2_tx_2, w1_tx_2],
            ),
            (
                reverse(self.url_list, query={"filter[amount.lt]": f"{w2_tx_2.amount}"}),
                [w2_tx_1, w1_tx_1],
            ),
            (
                reverse(self.url_list, query={"filter[amount.lte]": f"{w2_tx_2.amount}"}),
                [w3_tx_2, w2_tx_2, w2_tx_1, w1_tx_2, w1_tx_1],
            ),
            (
                reverse(self.url_list, query={"filter[amount.gt]": f"{w1_tx_2.amount}"}),
                [w3_tx_3],
            ),
            (
                reverse(self.url_list, query={"filter[amount.gte]": f"{w1_tx_2.amount}"}),
                [w3_tx_3, w3_tx_2, w2_tx_2, w1_tx_2],
            ),
            # # sorting:
            (
                reverse(self.url_list, query={"sort": "-amount"}),
                [w3_tx_3, w3_tx_2, w2_tx_2, w1_tx_2, w2_tx_1, w1_tx_1],
            ),
            (
                reverse(self.url_list, query={"sort": "amount"}),
                [w1_tx_1, w2_tx_1, w1_tx_2, w2_tx_2, w3_tx_2, w3_tx_3],
            ),
        )

        for url, expected in test_cases:
            with self.subTest(msg=f"Testing {url}"):
                request = self.factory.get(url)
                with CaptureQueriesContext(connection) as ctx:
                    response = self.view_list(request)
                # logger.info(ctx.captured_queries)
                self.assertEqual(len(ctx.captured_queries), 2)
                self.assertEqual(response.status_code, 200, response.data)
                expected_data = self.view_cls.serializer_class(expected, many=True).data
                self.assertListEqual(expected_data, response.data["results"])

    def test__sql(self):
        w1 = WalletFactory()
        w2 = WalletFactory()
        w3 = WalletFactory()

        w1_txs = [TransactionNoSignalsFactory(wallet=w1) for _ in range(25)]
        w2_txs = [TransactionNoSignalsFactory(wallet=w2) for _ in range(15)]
        w3_txs = [TransactionNoSignalsFactory(wallet=w3) for _ in range(15)]
        # other_txs = [TransactionNoSignalsFactory() for _ in range(500)]

        url = reverse(self.url_list, query="")  # default query
        request = self.factory.get(url)
        with CaptureQueriesContext(connection) as ctx:
            response = self.view_list(request)

        self.assertEqual(response.status_code, 200, response.data)
        logger.info(ctx.captured_queries)
        self.assertEqual(len(ctx.captured_queries), 2)
