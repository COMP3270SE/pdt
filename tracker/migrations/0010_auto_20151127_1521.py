# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20151127_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='developer',
            old_name='name',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='manager',
            old_name='name',
            new_name='username',
        ),
    ]
