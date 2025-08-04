from rest_framework import viewsets, mixins
from models.finances.models import Wallet, Transaction
from .filters import TransactionFilter, WalletFilter
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_class = WalletFilter

    # Fields available for sorting via `?sort=...`
    ordering_fields = ("label", "balance")

    # # Fields available for searching via `filter[search]=...`
    # search_fields = ("label",)


class TransactionViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter

    # Fields available for sorting via `?sort=...`
    ordering_fields = ("wallet", "txid", "amount")

    # # Fields available for searching via `filter[search]=...`
    # search_fields = ("txid",)
