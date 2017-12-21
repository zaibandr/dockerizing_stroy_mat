# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment_app', '0005_auto_20171122_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='documents_returned',
            field=models.CharField(choices=[('Y', 'Вернулись'), ('N', 'Нужны документы'), ('S', 'Скан')], default='N', max_length=4, verbose_name='Документы (вернулись)'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='have_document',
            field=models.CharField(choices=[('Y', 'Есть'), ('N', 'Нет'), ('N', 'Скан')], default='N', max_length=4, verbose_name='Документы (есть)'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='invoice_number',
            field=models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='Номер счет-фактуры'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payment',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Основание оплаты'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='ttn',
            field=models.NullBooleanField(verbose_name='Наличие транспортной накладной'),
        ),
    ]