# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20151129_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='defect',
            old_name='in_iteration',
            new_name='injection_iteration',
        ),
        migrations.RenameField(
            model_name='defect',
            old_name='out_iteration',
            new_name='removal_iteration',
        ),
    ]
