# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_question_question_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='message',
            field=models.TextField(),
        ),
    ]