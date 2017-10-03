from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="Name")


class Card(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    description = models.CharField(max_length=300, verbose_name="Description")
    list = models.ForeignKey('List', null=True)
