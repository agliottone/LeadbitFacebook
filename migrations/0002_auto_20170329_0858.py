# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leadbit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campagna',
            name='country',
            field=models.CharField(default=b'IT', max_length=255),
        ),
        migrations.AddField(
            model_name='campagna',
            name='flow_hash',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='campagna',
            name='landing',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='campagna',
            name='api',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='campagna',
            name='rss',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
