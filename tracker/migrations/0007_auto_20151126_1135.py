# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workrecord',
            name='date',
        ),
        migrations.AddField(
            model_name='workrecord',
            name='iteration',
            field=models.ForeignKey(default=datetime.datetime(2015, 11, 26, 11, 35, 52, 8726, tzinfo=utc), to='tracker.Iteration'),
            preserve_default=False,
        ),
    ]
