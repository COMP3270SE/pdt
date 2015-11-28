# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='iteration_id',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='phase',
            name='phase_id',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='pid',
            field=models.AutoField(default=0, serialize=False, primary_key=True),
        ),
    ]
