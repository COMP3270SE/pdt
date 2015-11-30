# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20151129_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='est_effort',
            field=models.FloatField(default=0.0),
        ),
    ]
