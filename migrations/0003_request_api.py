# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadbit', '0002_auto_20170329_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='api',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
