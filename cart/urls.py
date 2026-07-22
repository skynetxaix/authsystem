from django.urls import path
from .views import AddToCartView, ViewCartView, RemoveFromCartView

urlpatterns = [
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/", ViewCartView.as_view(), name="view-cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
]