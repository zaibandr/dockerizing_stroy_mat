# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment_app', '0003_auto_20171109_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipment',
            old_name='volume',
            new_name='volume_b',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='delivered',
        ),
        migrations.AddField(
            model_name='shipment',
            name='deliver',
            field=models.DateField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='volume_m',
            field=models.IntegerField(default=10, verbose_name='Объем'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='volume_s',
            field=models.IntegerField(default=10, verbose_name='Объем'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='confirmed',
            field=models.DateField(blank=True, null=True, verbose_name='Дата Подтверждения'),
        ),
    ]