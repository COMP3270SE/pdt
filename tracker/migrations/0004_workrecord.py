# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20151118_1526'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Workrecord',
        #     fields=[
        #         ('wid', models.IntegerField(default=0, serialize=False, primary_key=True)),
        #         ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
        #         ('starttime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
        #         ('endtime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
        #         ('developer', models.ForeignKey(to='tracker.Developer')),
        #     ],
        # ),
    ]
