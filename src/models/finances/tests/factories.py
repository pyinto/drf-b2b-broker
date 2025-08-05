from decimal import Decimal
import factory


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "finances.Wallet"

    balance = Decimal("0.000000000000000000")
    label = factory.Faker("name")

    def __new__(cls, *args, **kwargs) -> "WalletFactory.Meta.model":
        return super().__new__(*args, **kwargs)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "finances.Transaction"

    amount = factory.Faker("pydecimal", left_digits=60, right_digits=18)
    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Faker("uuid4")

    def __new__(cls, *args, **kwargs) -> "WalletFactory.Meta.model":
        return super().__new__(*args, **kwargs)


# todo: disable signals
# @factory.django.mute_signals(signals.pre_save, signals.post_save, signals.post_delete)
class TransactionNoSignalsFactory(TransactionFactory):
    """
    Same as TransactionFactory, but without signals.
    """

    def __new__(cls, *args, **kwargs) -> "WalletFactory.Meta.model":
        return super().__new__(*args, **kwargs)
