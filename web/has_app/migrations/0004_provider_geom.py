# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 16:50
from __future__ import unicode_literals

from django.db import migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('has_app', '0003_auto_20170809_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='geom',
            field=djgeojson.fields.PolygonField(default='[]'),
        ),
    ]