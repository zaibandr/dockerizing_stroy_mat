# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-25 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('has_app', '0003_auto_20170725_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Стоимость'),
        ),
    ]
