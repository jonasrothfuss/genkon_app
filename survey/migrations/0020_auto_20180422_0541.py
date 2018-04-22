# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-22 03:41
from __future__ import unicode_literals

import custom_storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0019_auto_20171111_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_image',
            field=models.ImageField(storage=custom_storages.MediaStorage(), upload_to='services'),
        ),
    ]
