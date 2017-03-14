# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 18:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0015_auto_20170306_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attraction_id', models.IntegerField()),
                ('attraction_name', models.CharField(default='', max_length=2000)),
                ('attraction_event_name', models.CharField(default='', max_length=2000)),
                ('attraction_start_ts', models.DateTimeField()),
            ]),
    ]