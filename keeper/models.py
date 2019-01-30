import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    password = models.CharField(max_length=200)
    card_id = models.IntegerField(default=8000000000)


class Key(models.Model):
    room_num = models.IntegerField()


class History(models.Model):
    key = models.IntegerField()
    time_cr = models.DateTimeField(default=timezone.now)
    # user_id = models.CharField(max_length=100)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.key


# Create your models here.
