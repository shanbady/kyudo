# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import autoslug.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freebase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.TextField(help_text=b'Edit in Markdown')),
                ('text_rendered', models.TextField(editable=False)),
                ('author', models.ForeignKey(related_name='answers', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(related_name='answers', to='fugato.Answer')),
                ('related', models.ManyToManyField(related_name='related_rel_+', to='fugato.Answer')),
            ],
            options={
                'db_table': 'answers',
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.CharField(max_length=512)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('hash', models.CharField(unique=True, max_length=28, editable=False)),
                ('details', models.TextField(default=None, help_text=b'Edit in Markdown', null=True, blank=True)),
                ('details_rendered', models.TextField(default=None, null=True, editable=False, blank=True)),
                ('parse', models.TextField(default=None, null=True, editable=False, blank=True)),
                ('author', models.ForeignKey(related_name='questions', to=settings.AUTH_USER_MODEL)),
                ('related', models.ManyToManyField(related_name='related_rel_+', editable=False, to='fugato.Question')),
                ('template', models.ForeignKey(related_name='questions', default=None, blank=True, editable=False, to='freebase.TextTemplate', null=True)),
                ('topics', models.ManyToManyField(related_name='questions', through='freebase.TopicAnnotation', to='freebase.Topic')),
            ],
            options={
                'db_table': 'questions',
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
    ]
