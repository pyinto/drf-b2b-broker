from django_filters import rest_framework as filters
from models.finances.models import Transaction, Wallet


class WalletFilter(filters.FilterSet):
    class Meta:
        model = Wallet
        fields = {
            "id": ["exact", "in"],  # TODO: we might not want to expose incremental ID for end user;
            "label": ["exact", "icontains"],
            "balance": ["exact", "range", "lt", "lte", "gt", "gte"],
        }


class TransactionFilter(filters.FilterSet):
    wallet_id = filters.BaseInFilter(field_name="wallet__id", lookup_expr="in")

    class Meta:
        model = Transaction
        fields = {
            "id": ["exact", "in"],  # TODO: we might not want to expose incremental ID for end user;
            "txid": ["exact", "icontains", "in"],
            "amount": ["exact", "range", "lt", "lte", "gt", "gte"],
        }
