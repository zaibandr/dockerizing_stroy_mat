# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment_app', '0002_auto_20171029_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='transporter',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Перевозчик'),
        ),
    ]
