# Generated by Django 2.1.5 on 2019-02-04 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='memo',
            field=models.CharField(default='', max_length=200),
        ),
    ]
