# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0013_auto_20170306_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='similarattractions',
            name='attraction',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='similarusers',
            name='user',
            field=models.IntegerField(),
        ),
    ]
