
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('users/', AccountList.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginToken.as_view()),
    path('logout/', Logout.as_view()),
    path('users/<int:pk>/', AccountDetail.as_view()),
    path('profile/<int:pk>/', ProfileDetail.as_view()),
    
]

