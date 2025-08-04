from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.query_utils import Q

from models.finances.querysets import TransactionManager, WalletManager, TransactionQuerySet, WalletQuerySet


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(
        max_digits=78,
        decimal_places=18,
        default=Decimal("0.000000000000000000"),
        validators=[
            MinValueValidator(Decimal("0.0")),
        ],
    )

    """
    Note: I would consider using custom Primary Key field here:
        1) uuid7   - Great choice: has timestamp metadata, fast inserts (indexing takes the same time as big int);
        2) uuid4   - If we don't want to expose timestamp metadata for end user (slower inserts due to char indexing);
        3) Big Int - If we don't care about exposure of incremental value to the end user,
           and we want to have creation date as separate field;

    """

    objects = WalletManager.from_queryset(WalletQuerySet)()

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

        ordering = ["id"]

        constraints = [
            # # db lvl constraint for min balance value:
            models.CheckConstraint(check=Q(balance__gte=0), name="balance_gte_0"),
            # models.CheckConstraint(check=Q(transactions__amount__sum__gte=0), name="tx_sum_gte_0")
        ]

        indexes = [
            # # Single-field indexes:
            models.Index(fields=["label"], name="idx-Wallet:label"),
            models.Index(fields=["balance"], name="idx-Wallet:balance"),
            # # Composite indexes for combined filtering/sorting:
            models.Index(fields=["label", "balance"], name="idx-Wallet:label-balance"),
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: id={self.id}, label={self.label!r}"

    def save(self, *args, **kwargs):
        self.full_clean()  # run all validators on .save()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    txid = models.CharField(max_length=255, unique=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(
        max_digits=78,
        decimal_places=18,
    )

    """
    Note: I would consider using custom Primary Key field here:
        1) uuid7   - Great choice: has timestamp metadata, fast inserts (indexing takes the same time as big int);
        2) uuid4   - If we don't want to expose timestamp metadata for end user (slower inserts due to char indexing);
        3) Big Int - If we don't care about exposure of incremental value to the end user,
           and we want to have creation date as separate field;
        4*) Also, we can consider usage of txid as pk, need more info of what it consists of;
    """

    objects = TransactionManager.from_queryset(TransactionQuerySet)()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

        ordering = ["-id"]  # newest transactions first;

        indexes = [
            # # Single-field indexes:
            models.Index(fields=["amount"], name="idx-Transaction:amount"),
            # # Composite indexes for combined filtering/sorting:
            models.Index(fields=["wallet_id", "amount"], name="idx-Transaction:wallet-amount"),
            models.Index(fields=["wallet_id", "id"], name="idx-Transaction:wallet-id"),
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: id={self.id}, wallet_id={self.wallet_id}"
