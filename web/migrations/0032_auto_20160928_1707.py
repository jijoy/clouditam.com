# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 14:07
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0031_auto_20160905_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='asset_limit',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='details',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='plan_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=64, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='type',
            field=models.CharField(blank=True, choices=[('Monthly', 'Monthly'), ('Annually', 'Annually'), ('Free', 'Free')], default='Monthly', max_length=64),
        ),
    ]
