# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-15 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_auto_20170513_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='accepted_terms',
            field=models.BooleanField(default=False, verbose_name='Einverständnis'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Datum'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='selected_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Service', verbose_name='Gewähltes Ehrenamt'),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_description',
            field=models.CharField(max_length=2000),
        ),
    ]
