# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_auto_20160818_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.DashUser'),
        ),
    ]
