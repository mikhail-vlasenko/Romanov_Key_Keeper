# Generated by Django 2.1.5 on 2019-03-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeper', '0005_auto_20190215_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='key_tran_last',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_tran_last',
            field=models.CharField(default='никто', max_length=255),
        ),
    ]
