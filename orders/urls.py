from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from .views import CreateOrderView
router = DefaultRouter()

router.register("orders", OrderViewSet)

urlpatterns = router.urls
path(
    "orders/create/",
    CreateOrderView.as_view(),
    name="create-order"
),
