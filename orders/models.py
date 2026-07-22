from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from products.models import Product


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethod(models.TextChoices):
    WALLET = "wallet", "Wallet"
    GATEWAY = "gateway", "Gateway"

class Order(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    quantity = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
    max_length=20,
    choices=OrderStatus.choices,
    default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
    max_length=20,
    choices=PaymentMethod.choices,
    null=True,
    blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    tracking_code = models.CharField(
        max_length=100,
        blank=True
    )
        

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    