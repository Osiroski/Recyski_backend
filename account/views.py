from django.http.response import Http404
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

# Create your views here.
from .models import Account, Profile
from .serializers import AccountSerializer, LoginSerializer, ProfileSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status

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


class ProfileDetail(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404
    #GET METHOD
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #UPDATE METHOD
    def put(self, request,pk, **kwargs):
        partial = kwargs.pop('partial', False)
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
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


