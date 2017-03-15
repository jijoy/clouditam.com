# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0020_auto_20160811_2318'),
        ('dashboard', '0002_auto_20160730_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='asset',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='company',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='dashuser',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='hardware',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='location',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='status',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Customer'),
        ),
    ]