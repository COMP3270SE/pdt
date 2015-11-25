# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20151124_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='iteration',
        ),
        migrations.AddField(
            model_name='defect',
            name='in_iteration',
            field=models.ForeignKey(related_name='injection', default=1, to='tracker.Iteration'),
        ),
        migrations.AddField(
            model_name='defect',
            name='out_iteration',
            field=models.ForeignKey(related_name='removal', default=1, to='tracker.Iteration'),
        ),
    ]
