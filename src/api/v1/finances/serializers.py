from rest_framework_json_api import serializers
from rest_framework_json_api.relations import (
    ResourceRelatedField,
    SerializerMethodFieldBase,
)
from rest_framework_json_api.utils import format_resource_type

from models.finances.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "label",
            "balance",
        )


class WalletResourceRelatedField(SerializerMethodFieldBase, ResourceRelatedField):
    resource_type = format_resource_type(Wallet.__name__)

    def to_representation(self, instance):
        pk = self.get_resource_id(instance)
        return {"type": self.resource_type, "id": str(pk)}


class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletResourceRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "txid",
            "amount",
            "wallet",
        )

    def get_wallet(self, instance) -> Wallet:
        # Mocking Wallet instance with only 'id' field loaded, to skip extra SQL queries
        return Wallet(id=instance.wallet_id)
