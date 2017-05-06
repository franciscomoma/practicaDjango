# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-01 14:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_auto_20170501_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
