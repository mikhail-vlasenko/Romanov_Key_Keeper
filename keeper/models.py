import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    password = models.CharField(max_length=200)
    card_id = models.IntegerField(default=8000000000)


class History(models.Model):
    key = models.IntegerField()
    time_cr = models.DateTimeField(default=datetime.datetime.now)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    time_back = models.DateTimeField(default=datetime.datetime.min)

