# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('has_app', '0012_auto_20170829_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsnotify',
            name='resp',
        ),
        migrations.AddField(
            model_name='smsnotify',
            name='sms_id',
            field=models.IntegerField(default=0),
        ),
    ]