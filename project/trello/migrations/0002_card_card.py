# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-23 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trello.List'),
        ),
    ]
