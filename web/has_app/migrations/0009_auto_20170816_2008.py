# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('has_app', '0008_auto_20170814_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CRTD', 'Создан'), ('PRCSG', 'На отгрузке'), ('CMPLTD', 'Отгружено')], default='CRTD', max_length=7, verbose_name='Статус')),
                ('customer', models.CharField(max_length=100, verbose_name='Покупатель')),
                ('transporter', models.CharField(max_length=100, verbose_name='Перевозчик')),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Адрес')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('volume', models.IntegerField(default=10, verbose_name='Объем')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('cost_in', models.IntegerField(default=0, verbose_name='Стоимость (входящая)')),
                ('cost_out', models.IntegerField(default=0, verbose_name='Стоимость (продажная)')),
                ('profit', models.IntegerField(default=0, verbose_name='Прибыль')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('time_completed', models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product',
                 models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='has_app.Product')),
            ],
            options={
                'verbose_name_plural': 'Отгрузки',
                'verbose_name': 'Отгрузка',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='volume',
            field=models.IntegerField(default=10, verbose_name='Объем'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='contact_name',
            field=models.TextField(max_length=100, verbose_name='Контактное лицо'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='provider',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='has_app.Provider',
                                    verbose_name='Поставщик'),
        ),
    ]
