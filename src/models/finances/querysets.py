from django.db import models


class WalletManager(models.Manager):
    def get_queryset(self):
        return WalletQuerySet(self.model, using=self._db)


class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)


class WalletQuerySet(models.QuerySet):
    """ """

    # todo: add queries


class TransactionQuerySet(models.QuerySet):
    """ """

    # todo: add queries
