# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-11 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0016_profile_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('open', 'offen'), ('accepted', 'aufgenommen'), ('cancelled', 'abgebrochen')], max_length=30, verbose_name='Status'),
        ),
    ]
