# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_account_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='price_detail',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
