from decimal import Decimal
import django.core.exceptions
import django.db.utils
from django.test import TestCase
from django.db import transaction
from models.finances.models import Wallet, Transaction
from models.finances.tests.factories import WalletFactory, TransactionFactory, TransactionNoSignalsFactory


class WalletModelTestCase(TestCase):
    def test__create(self):
        create_kwargs = dict(label="test")
        instance = Wallet.objects.create(**create_kwargs)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.label, create_kwargs["label"])
        self.assertIsInstance(instance.balance, Decimal)
        self.assertEqual(instance.balance, Decimal("0.0"))

    def test__factory(self):
        instance = WalletFactory()
        self.assertIsNotNone(instance.id)
        self.assertIsInstance(instance.label, str)
        self.assertIsInstance(instance.balance, Decimal)
        self.assertEqual(instance.balance, Decimal("0.0"))

    def test__balance_validation__err(self):
        instance = WalletFactory(balance=Decimal("1.0"))
        instance.balance = Decimal("-1.0")  # setting negative value to trigger err

        with transaction.atomic():
            with self.assertRaises(django.core.exceptions.ValidationError) as cm:
                instance.save()

        exception = cm.exception
        self.assertEqual(exception.messages, ["Ensure this value is greater than or equal to 0.0."])
        instance.refresh_from_db()
        self.assertEqual(instance.balance, Decimal("1.0"))

    def test__balance_validation__success(self):
        instance = WalletFactory(balance=Decimal("1.111111111111111111"))
        instance.balance = instance.balance + Decimal("2.222222222222222222")
        instance.save()
        instance.refresh_from_db()
        self.assertEqual(instance.balance, Decimal("3.333333333333333333"))


class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.wallet = WalletFactory()

        # # Max ETH values:
        self.max_uint256_in_wei = 2**256 - 1  # The maximum value of a uint256 is 2**256 - 1
        self.max_eth_value = Decimal(self.max_uint256_in_wei) / Decimal(10) ** 18  # max ETH value (10^18 Wei)
        self.max_eth_value_negative = -self.max_eth_value

        # # Max DB value supported:
        self.max_digits, self.decimal_places = 78, 18
        self.max_db_value = Decimal(f"{'9' * (self.max_digits - self.decimal_places)}.{'9' * self.decimal_places}")
        self.max_db_value_negative = Decimal(f"-{self.max_db_value}")

    def test__create(self):
        create_kwargs = dict(
            txid="test-123456789",
            wallet=self.wallet,
            amount=Decimal("1.0"),
        )
        instance = Transaction.objects.create(**create_kwargs)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.txid, create_kwargs["txid"])
        self.assertEqual(instance.wallet.id, create_kwargs["wallet"].id)
        self.assertEqual(instance.amount, create_kwargs["amount"])

    def test__factory(self):
        instance = TransactionNoSignalsFactory()
        instance.refresh_from_db()
        self.assertIsNotNone(instance.id)
        self.assertIsInstance(instance.txid, str)
        self.assertIsInstance(instance.amount, Decimal)
        self.assertIsInstance(instance.wallet, Wallet)

    def test__max_amount_validation__success(self):
        test_cases = (
            (self.max_eth_value, "positive max ETH"),
            (self.max_eth_value_negative, "negative max ETH"),
            (self.max_db_value, "positive max db value"),
            (self.max_db_value_negative, "negative max db value"),
        )

        for target_amount, desc in test_cases:
            with self.subTest(msg=f"Testing '{desc}', value: '{target_amount}' ..."):
                instance = TransactionNoSignalsFactory(amount=target_amount)
                instance.refresh_from_db()
                self.assertEqual(instance.amount, target_amount)

    def test__max_amount_validation__err(self):
        test_cases = (
            (self.max_db_value + Decimal("1"), "max db value +1"),
            (self.max_db_value_negative - Decimal("1"), "max db value -1"),
        )

        for target_amount, desc in test_cases:
            with self.subTest(msg=f"Testing '{desc}', value: '{target_amount}' ..."):
                with transaction.atomic():
                    with self.assertRaises(django.db.utils.DataError) as cm:
                        TransactionNoSignalsFactory(amount=target_amount)

                    exception = cm.exception
                    self.assertEqual(
                        exception.__str__(),
                        "numeric field overflow\n"
                        "DETAIL:  A field with precision 78, scale 18 must round to an absolute value less than 10^60.",
                    )
