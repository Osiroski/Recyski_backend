from django.http.response import Http404
from django.shortcuts import render
from django.views import generic
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from .backends import CaseInsensitiveModelBackend

# Create your views here.
from .models import Account, History, Profile
from .serializers import AccountSerializer, HistorySerializer, LoginSerializer, ProfileSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AccountList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class RegisterView(APIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        data = {
            "password":make_password(password=request.data["password"], hasher='default'),
            "email":request.data['email'],
            "username":request.data['username'],
            "first_name":request.data['first_name'],
            "last_name":request.data['last_name']
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        try:
            return Profile.objects.get(user=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginToken(APIView):
    queryset = Account.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = authenticate(request,
                            username=serializer.data['email'],
                            password=serializer.data["password"])
        if user is not None:
            login(request,
                  user,
                  backend='account.backends.CaseInsensitiveModelBackend')
            token, created = Token.objects.get_or_create(user=user)

        else:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': user.auth_token.key,
                'active': user.is_active,
                'last_login': user.last_login
            },
            status=status.HTTP_200_OK)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        if request.user.is_authenticated:
            request.user.auth_token.delete()
        return Response('User Logged out successfully',
                        status=status.HTTP_200_OK)


class HistoryList(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_object(self, pk):
        try:
            return History.objects.get(user=pk)
        except History.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        data = History.objects.filter(user=pk)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        history = self.get_object(pk)
        history.delete()
        return Response('Successfully Deleted',
                        status=status.HTTP_204_NO_CONTENT)
