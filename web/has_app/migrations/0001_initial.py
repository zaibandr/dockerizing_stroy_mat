# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-04 18:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.IntegerField(default=3, verbose_name='Объем')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('status', models.CharField(choices=[('CRTD', 'Создан'), ('PRCSD', 'В обработке'), ('CMPLTD', 'Обработан')], default='CRTD', max_length=7, verbose_name='Статус')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=12, null=True, verbose_name='Телефон')),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Адрес')),
                ('tonar', models.IntegerField(choices=[(1, 'Дa'), (0, 'Нет')], default='Нет', verbose_name='Тонары')),
                ('time_of_receipt', models.IntegerField(choices=[(2, 'Круглосуточно'), (0, 'День'), (1, 'Ночь')], default='День', verbose_name='Время приема')),
                ('payment', models.IntegerField(choices=[(0, 'Безналичный'), (1, 'Наличный')], default='Наличный', verbose_name='Расчет')),
                ('cost', models.IntegerField(default=0, verbose_name='Стоимость')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('time_completed', models.DateTimeField(blank=True, null=True, verbose_name='Дата обработки')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('coordinate', models.CharField(blank=True, max_length=100, null=True, verbose_name='Координаты')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Наименование',
                'verbose_name_plural': 'Наименования',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('contact_name', models.TextField(max_length=100, verbose_name='Контактное лицо')),
                ('phone_number', models.CharField(max_length=12, null=True, verbose_name='Телефон')),
                ('geo_json', models.TextField(verbose_name='GeoJson')),
                ('products', models.ManyToManyField(to='has_app.Product', verbose_name='Продукция')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('polygon', models.TextField(verbose_name='Полигон')),
            ],
            options={
                'verbose_name': 'Зона',
                'verbose_name_plural': 'Зоны',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='has_app.Product'),
        ),
    ]