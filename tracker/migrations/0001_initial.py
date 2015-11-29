# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(default=b'M', max_length=2, choices=[(b'SU', b'Super User'), (b'M', b'Manager'), (b'D', b'Developer')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('did', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('type', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('uid', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('SLOC', models.IntegerField(default=0)),
                ('iteration_id', models.AutoField(serialize=False, primary_key=True)),
                ('time_length', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('uid', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('type', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('phase_id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('pid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('est_SLOC', models.IntegerField(default=0)),
                ('est_escape', models.FloatField(default=0.0)),
                ('developer', models.ManyToManyField(to='tracker.Developer')),
                ('manager', models.ForeignKey(to='tracker.Manager')),
            ],
        ),
        migrations.CreateModel(
            name='Workrecord',
            fields=[
                ('wid', models.IntegerField(default=0, serialize=False, primary_key=True)),
                ('starttime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('endtime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('developer', models.ForeignKey(to='tracker.Developer')),
                ('iteration', models.ForeignKey(to='tracker.Iteration')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='tracker.Project'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='phase',
            field=models.ForeignKey(to='tracker.Phase'),
        ),
        migrations.AddField(
            model_name='defect',
            name='developer',
            field=models.ForeignKey(to='tracker.Developer'),
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
