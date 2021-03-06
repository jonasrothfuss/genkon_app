# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-12 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_auto_20170503_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='empty_profile',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='selected_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Service', verbose_name='Gewählter Service'),
        ),
    ]
