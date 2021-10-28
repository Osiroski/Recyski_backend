from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage, send_mail

from .managers import MyAccountManager


# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username=models.CharField(max_length=10,unique=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    first_name = models.CharField(verbose_name="first name",max_length=30, blank=True)
    last_name = models.CharField(verbose_name="last name",max_length=30, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    objects=MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']

    def __str__(self) -> str:
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phoneNumber=PhoneNumberField(null=True,blank=True)
    points=models.IntegerField(default=50)
    level = models.TextField(max_length=500, blank=True)
    def __str__(self) -> str:
        return self.user.username
@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


   

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_mail_on_create(sender, instance, created=False, **kwargs):
    if created:
        activate_link_url='http//:127.0.0.1:8000/'
        actiavation_link = f'{activate_link_url}?user_id={instance.id}&confirmation_token={instance.auth_token}'
        send_mail(
    'Recyski Registration',
    f'You are receiving this mail because you registered on the Recyski Platform.\n Please click the lick below to confirm your account\n {actiavation_link}',
    'recyski@example.com',
    [instance.email]
    ) # call send mail function



class History(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    date = models.DateField(null=True, blank=True)
    points=models.IntegerField(default=50)
    units=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username