# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20160817_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='is_os',
            field=models.BooleanField(default=False),
        ),
    ]
