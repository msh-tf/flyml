# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 19:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0019_attraction_attraction_event_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='attraction_event_name',
        ),
    ]