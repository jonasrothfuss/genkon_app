# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20170424_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Erstellugsdatum'),
        ),
    ]