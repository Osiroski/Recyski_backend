from rest_framework import serializers
from .models import Account,Profile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','email','username','first_name','last_name']
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','username','first_name','last_name','password']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

