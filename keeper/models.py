import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Key(models.Model):
    room_num = models.IntegerField()


class History(models.Model):
    key = models.IntegerField()
    time_cr = models.DateTimeField(default=timezone.now)
    user_id = models.CharField(max_length=100)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.key


# Create your models here.
