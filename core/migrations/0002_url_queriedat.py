# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 21:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='queriedAt',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 3, 21, 49, 32, 538665, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
