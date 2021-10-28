from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password):
        if not email:
            raise ValueError("Users must have an Email Address")
        if not username:
            raise ValueError("Users must have a username")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user