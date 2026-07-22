from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import Order, OrderStatus, PaymentMethod
from .serializers import OrderSerializer, CreateOrderSerializer
from products.models import Product
import requests
from django.conf import settings
from django.shortcuts import redirect


class PayWithGatewayView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != OrderStatus.PENDING:
            return Response({"error": "This order is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        amount_rial = int(order.total_price) * 10  # تومان به ریال

        response = requests.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            json={
                "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                "amount": amount_rial,
                "callback_url": settings.ZARINPAL_CALLBACK_URL,
                "description": f"Payment for order #{order.id}"
            }
        )
        data = response.json()

        if data["data"]["code"] != 100:
            return Response({"error": "Gateway request failed"}, status=status.HTTP_400_BAD_REQUEST)

        authority = data["data"]["authority"]
        order.tracking_code = authority
        order.save()

        pay_url = f"https://sandbox.zarinpal.com/pg/StartPay/{authority}"
        return Response({"payment_url": pay_url})


class VerifyPaymentView(APIView):
    def get(self, request):
        authority = request.GET.get("Authority")
        gateway_status = request.GET.get("Status")

        try:
            order = Order.objects.get(tracking_code=authority)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if gateway_status != "OK":
            order.status = OrderStatus.CANCELLED
            order.save()
            return Response({"error": "Payment cancelled by user"}, status=status.HTTP_400_BAD_REQUEST)

        amount_rial = int(order.total_price) * 10

        response = requests.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
            json={
                "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                "amount": amount_rial,
                "authority": authority
            }
        )
        data = response.json()

        if data["data"]["code"] in [100, 101]:
            order.status = OrderStatus.PAID
            order.payment_method = PaymentMethod.GATEWAY
            order.paid_at = timezone.now()
            order.product.stock -= order.quantity
            order.product.save()
            order.save()
            return Response({"message": "Payment verified", "order_id": order.id})
        else:
            order.status = OrderStatus.CANCELLED
            order.save()
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=serializer.validated_data["product"])
        quantity = serializer.validated_data["quantity"]

        if product.stock < quantity:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = product.price * quantity

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            status=OrderStatus.PENDING
        )

        return Response(
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )
    


class PayWithWalletView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status != OrderStatus.PENDING:
            return Response({"error": "This order is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = request.user.wallet

        if wallet.balance < order.total_price:
            return Response({"error": "Insufficient wallet balance"}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= order.total_price
        wallet.save()

        order.product.stock -= order.quantity
        order.product.save()

        order.status = OrderStatus.PAID
        order.payment_method = PaymentMethod.WALLET
        order.paid_at = timezone.now()
        order.save()

        return Response({"message": "Payment successful", "order_id": order.id, "status": order.status})



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)