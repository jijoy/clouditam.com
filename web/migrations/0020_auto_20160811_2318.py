# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_auto_20160811_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='apps',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='users',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='address2',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='company_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='fullname',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='zip_or_postal',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]