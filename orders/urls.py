from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    CreateOrderView,
    PayWithWalletView,
    PayWithGatewayView,
    VerifyPaymentView,
)

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
urlpatterns = router.urls + [
    path("orders/create/", CreateOrderView.as_view(), name="create-order"),
    path("orders/<int:order_id>/pay-wallet/", PayWithWalletView.as_view(), name="pay-wallet"),
    path("orders/<int:order_id>/pay-gateway/", PayWithGatewayView.as_view(), name="pay-gateway"),
    path("orders/verify/", VerifyPaymentView.as_view(), name="verify-payment"),
]