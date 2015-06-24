# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'templates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mid', models.CharField(unique=True, max_length=32)),
                ('title', models.CharField(max_length=512)),
                ('notability', models.CharField(default=None, max_length=512, null=True, blank=True)),
                ('image', models.URLField(default=None, max_length=2000, null=True, blank=True)),
                ('attrs', jsonfield.fields.JSONField(default=None, null=True, blank=True)),
                ('description', models.TextField(default=None, null=True, blank=True)),
            ],
            options={
                'db_table': 'topics',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'annotations',
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
    ]
