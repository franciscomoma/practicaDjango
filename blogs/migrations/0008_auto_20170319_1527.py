# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_auto_20170318_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.FilePathField(blank=True, match='.+(.png|.jpg)$', null=True, path='static/uploads'),
        ),
    ]
