# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 18:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.IntegerField(default=10, verbose_name='Объем')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('status',
                 models.CharField(choices=[('CRTD', 'Создан'), ('CMPLTD', 'Обработан')], db_index=True, default='CRTD',
                                  max_length=7, verbose_name='Статус')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=60, null=True, verbose_name='Телефон')),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Адрес')),
                ('tonar', models.IntegerField(choices=[(1, 'Да'), (0, 'Нет')], default='Нет', verbose_name='Тонары')),
                ('time_of_receipt',
                 models.IntegerField(choices=[(2, 'Круглосуточно'), (0, 'День'), (1, 'Ночь')], default='День',
                                     verbose_name='Время приема')),
                ('payment', models.IntegerField(choices=[(0, 'Безналичный'), (1, 'Наличный')], default='Наличный',
                                                verbose_name='Расчет')),
                ('cost', models.IntegerField(default=0, verbose_name='Стоимость')),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('time_updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата изменения')),
                ('time_completed',
                 models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата обработки')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('coordinate', models.CharField(blank=True, max_length=100, null=True, verbose_name='Координаты')),
                (
                'manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Заказы',
                'verbose_name': 'Заказ',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=300, verbose_name='Наименование')),
            ],
            options={
                'verbose_name_plural': 'Наименования',
                'ordering': ['name'],
                'verbose_name': 'Наименование',
            },
        ),
        migrations.CreateModel(
            name='SmsNotify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_id', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_app.Order')),
                (
                'provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider_app.Provider')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order_app.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='provider',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='provider_app.Provider',
                                    verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='comment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_app.Order'),
        ),
    ]

