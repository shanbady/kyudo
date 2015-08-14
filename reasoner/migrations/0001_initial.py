# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fugato', '0004_auto_20150713_1111'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('started', models.DateTimeField(default=b'auto_now_add')),
                ('finished', models.DateTimeField(default=None, null=True, blank=True)),
                ('modified', models.DateTimeField(default=b'auto_now')),
                ('successful', models.NullBooleanField(default=None, help_text=b'the dialog was successful')),
                ('completed', models.BooleanField(default=False, help_text=b'user has finished the dialog')),
                ('terminated', models.BooleanField(default=False, help_text=b'dialog closed after inactivity')),
            ],
            options={
                'db_table': 'dialogues',
                'get_latest_by': 'started',
            },
        ),
        migrations.CreateModel(
            name='QuestionSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('is_subgoal', models.BooleanField(default=False)),
                ('dialogue', models.ForeignKey(related_name='series', to='reasoner.Dialogue')),
                ('parent_goal', models.ForeignKey(related_name='child_goals', default=None, blank=True, to='fugato.Question', null=True)),
                ('previous', models.ForeignKey(related_name='followups', default=None, blank=True, to='fugato.Question', null=True)),
                ('question', models.ForeignKey(related_name='series', to='fugato.Question')),
            ],
            options={
                'db_table': 'dialogue_question_series',
                'get_latest_by': 'created',
            },
        ),
        migrations.AddField(
            model_name='dialogue',
            name='questions',
            field=models.ManyToManyField(related_name='dialogues', through='reasoner.QuestionSeries', to='fugato.Question'),
        ),
        migrations.AddField(
            model_name='dialogue',
            name='user',
            field=models.ForeignKey(related_name='dialogues', to=settings.AUTH_USER_MODEL),
        ),
    ]
