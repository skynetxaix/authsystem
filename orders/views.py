from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from .serializers import CreateOrderSerializer
from .models import Order
class CreateOrderView(APIView):

    def post(self, request):

        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(
            id=serializer.validated_data["product"]
        )

        quantity = serializer.validated_data["quantity"]

        total_price = product.price * quantity

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        return Response(
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer