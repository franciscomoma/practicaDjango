# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-12 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20170312_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]