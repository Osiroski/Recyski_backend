"""recyski URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from account import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.views import Logout


# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Recyski API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.AccountList.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginToken.as_view()),
    path('logout/', Logout.as_view()),
    path('users/<int:pk>/', views.AccountDetail.as_view()),
    path('profile/<int:pk>/', views.ProfileDetail.as_view()),
    path('history/<int:pk>/', views.HistoryList.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]