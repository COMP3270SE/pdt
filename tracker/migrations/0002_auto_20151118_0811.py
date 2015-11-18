# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='id',
        ),
        migrations.RemoveField(
            model_name='developer',
            name='id',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='id',
        ),
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.AddField(
            model_name='defect',
            name='did',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='uid',
            field=models.IntegerField(serialize=False, primary_key=True, validators=[django.core.validators.MinValueValidator(10000000), django.core.validators.MaxValueValidator(49999999)]),
        ),
        migrations.AlterField(
            model_name='manager',
            name='uid',
            field=models.IntegerField(serialize=False, primary_key=True, validators=[django.core.validators.MinValueValidator(50000000), django.core.validators.MaxValueValidator(99999999)]),
        ),
        migrations.AlterField(
            model_name='project',
            name='pid',
            field=models.IntegerField(default=0, serialize=False, primary_key=True),
        ),
    ]
