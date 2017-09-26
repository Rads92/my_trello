from django.db import models


# Create your models here.


class List(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")


class Card(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    description = models.CharField(max_length=300, verbose_name="Description")
    list = models.ForeignKey('List', null=True)
