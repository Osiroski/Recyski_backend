from django.db import models
from django.conf import settings
import uuid

class SellOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=30, blank=True)
    unit = models.IntegerField()
    amount=models.IntegerField()
    item = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return self.user.username

class BuyOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=False,null=False)
    location = models.CharField(max_length=30, blank=True)
    unit = models.IntegerField()
    amount=models.IntegerField()
    item = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return self.user.username   
    
class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    item = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    date = models.DateField(null=True, blank=True)
    points=models.IntegerField(default=50)
    units=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username



  