from django.urls import path
from .views import *

urlpatterns = [
    path('buy/', BuyOrderList.as_view()),
    path('buy/<int:pk>/', BuyOrderDetail.as_view()),
    path('sell/', SellOrderList.as_view()),
    path('sell/<int:pk>/', SellOrderDetail.as_view()),
    path('history/', HistoryList.as_view()),
    path('history/<int:pk>/', HistoryDetail.as_view()), 
]

