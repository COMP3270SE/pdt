# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0013_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='account',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
