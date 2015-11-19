# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20151118_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='iteration',
            name='id',
        ),
        migrations.RemoveField(
            model_name='phase',
            name='id',
        ),
        migrations.AddField(
            model_name='iteration',
            name='iteration_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='phase',
            name='phase_id',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AddField(
            model_name='project',
            name='est_SLOC',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='phase',
            name='type',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
