# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20151130_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workrecord',
            name='wid',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
