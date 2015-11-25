# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20151125_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='est_escape',
            field=models.FloatField(default=0.0),
        ),
    ]
