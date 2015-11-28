# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20151128_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='pid',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
