# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='bg_image',
            field=models.ImageField(default='static/web/images/headers/index.jpg', upload_to='headers'),
        ),
        migrations.AddField(
            model_name='header',
            name='title',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
