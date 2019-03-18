import datetime
from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    User model

    :param card_id: Number of card
    :param key_tran_last: Number of room, which was offered to receive last. If there is no such, it = -1
    :param user_tran_last: Username of user, who offered to receive a key last. If there is no such, it = "никто"
    """
    card_id = models.IntegerField(default=8000000000)
    key_tran_last = models.IntegerField(default=-1)
    user_tran_last = models.CharField(max_length=255, default='никто')


class History(models.Model):
    """
    Model for storing key history

    :param key: Number of key
    :param time_cr: Date of creation
    :param user_id: User, who took a key
    :param active: Is user still using key
    :param time_back: Date of return
    """
    key = models.IntegerField()
    time_cr = models.DateTimeField(default=datetime.datetime.now)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.CharField(max_length=100, default='Не сдан')
    time_back = models.DateTimeField(default=datetime.datetime.min)

    def month_cr(self):
        return self.time_cr.strftime('%m')

    def date_cr(self):
        return self.time_cr.strftime('%d')

    def hour_cr(self):
        return self.time_cr.strftime('%H')

    def minute_cr(self):
        return self.time_cr.strftime('%M')

    def month_b(self):
        return self.time_back.strftime('%m')

    def date_b(self):
        return self.time_back.strftime('%d')

    def hour_b(self):
        return self.time_back.strftime('%H')

    def minute_b(self):
        return self.time_back.strftime('%M')
