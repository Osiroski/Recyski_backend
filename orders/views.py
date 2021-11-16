from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from rest_framework import generics
from .serializers import *

# Create your views here.
class BuyOrderList(generics.ListCreateAPIView):
    queryset = BuyOrder.objects.all()
    serializer_class = BuyOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['item']
    ordering_fields = ['item', 'date']

class BuyOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuyOrder.objects.all()
    serializer_class = BuyOrderSerializer

class SellOrderList(generics.ListCreateAPIView):
    queryset = SellOrder.objects.all()
    serializer_class = SellOrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['item']
    ordering_fields = ['item', 'date']

class SellOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellOrder.objects.all()
    serializer_class = SellOrderSerializer

class HistoryList(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['item']
    ordering_fields = ['item', 'date']

class HistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuyOrder.objects.all()
    serializer_class = BuyOrderSerializer

