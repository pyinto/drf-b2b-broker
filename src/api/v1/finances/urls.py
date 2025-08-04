from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, TransactionViewSet

app_name = "finances"


router = DefaultRouter()
router.register(r"wallets", WalletViewSet, basename="wallet")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    *router.urls,
]
