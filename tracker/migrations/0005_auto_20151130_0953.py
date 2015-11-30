# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workrecord',
            name='endtime',
        ),
        migrations.RemoveField(
            model_name='workrecord',
            name='starttime',
        ),
        migrations.AddField(
            model_name='workrecord',
            name='interval',
            field=models.FloatField(default=0.0),
        ),
    ]
