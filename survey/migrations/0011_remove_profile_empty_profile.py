# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-12 17:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_auto_20170512_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='empty_profile',
        ),
    ]
