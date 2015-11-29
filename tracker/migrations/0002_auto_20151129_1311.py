# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='developer',
            old_name='uid',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='manager',
            old_name='uid',
            new_name='id',
        ),
    ]
