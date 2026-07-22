from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer