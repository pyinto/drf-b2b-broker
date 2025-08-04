import random
from django.core.management.base import BaseCommand, CommandError
from models.finances.models import Transaction
from models.finances.tests.factories import WalletFactory, TransactionFactory


class Command(BaseCommand):
    help = "Generates Fake Data for Testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wallets-count",
            type=int,
            default=5,
            help="Number of wallets to create (default: 5)",
        )

        parser.add_argument(
            "--tx-range",
            nargs=2,  # Expects exactly two values
            type=int,
            default=[10, 100],  # Default must match nargs expectation (a list of 2 ints)
            help="Min and Max transactions per wallet (e.g., --tx-range 10 100). Default: 10 100",
        )

    def handle(self, *args, **options):
        wallets_count = options["wallets_count"]
        tx_range = options["tx_range"]

        tx_count_before = Transaction.objects.count()
        self.stdout.write(self.style.NOTICE(f"Going to create {wallets_count} wallets with {tx_range} tx per each..."))
        self.stdout.write(self.style.NOTICE(f"Transaction count before: {tx_count_before}."))

        for _ in range(wallets_count):
            wallet = WalletFactory()
            tx_count = random.randrange(*tx_range)
            for _ in range(tx_count):
                TransactionFactory(wallet=wallet)
            self.stdout.write(f" - {wallet} - {tx_count} transactions created...")

        tx_count_after = Transaction.objects.count()
        tx_count_created = tx_count_after - tx_count_before

        self.stdout.write(self.style.NOTICE(f"Transaction count after: {tx_count_after}."))
        self.stdout.write(self.style.SUCCESS(f"Successfully created {tx_count_created} transactions!"))
