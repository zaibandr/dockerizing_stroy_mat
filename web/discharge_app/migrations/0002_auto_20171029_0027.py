# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discharge_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dischargecustomer',
            name='action_date',
            field=models.CharField(default=None, max_length=20, verbose_name='Дата операции (из выписки)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dischargecustomer',
            name='document_id',
            field=models.IntegerField(default=None, unique=True, verbose_name='Номер документа (из выписки)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dischargeprovider',
            name='action_date',
            field=models.CharField(default=None, max_length=20, verbose_name='Дата операции (из выписки)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dischargeprovider',
            name='document_id',
            field=models.IntegerField(default=None, unique=True, verbose_name='Номер документа (из выписки)'),
            preserve_default=False,
        ),
    ]