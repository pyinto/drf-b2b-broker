from django.contrib import admin
from models.finances.models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """ """


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """ """
