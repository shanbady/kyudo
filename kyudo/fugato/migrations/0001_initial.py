# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(related_name=b'answers', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(related_name=b'answers', to='fugato.Answer')),
                ('related', models.ManyToManyField(related_name='related_rel_+', to='fugato.Answer')),
            ],
            options={
                'db_table': 'answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('vote', models.SmallIntegerField(choices=[(-1, b'downvote'), (1, b'upvote')])),
                ('answer', models.ForeignKey(related_name=b'votes', to='fugato.Answer')),
                ('user', models.ForeignKey(related_name=b'answer_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'answer_voting',
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
                ('hash', models.CharField(unique=True, max_length=28)),
                ('author', models.ForeignKey(related_name=b'questions', to=settings.AUTH_USER_MODEL)),
                ('related', models.ManyToManyField(related_name='related_rel_+', to='fugato.Question')),
            ],
            options={
                'db_table': 'questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('vote', models.SmallIntegerField(choices=[(-1, b'downvote'), (1, b'upvote')])),
                ('question', models.ForeignKey(related_name=b'votes', to='fugato.Question')),
                ('user', models.ForeignKey(related_name=b'question_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question_voting',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='voters',
            field=models.ManyToManyField(related_name=b'+', through='fugato.QuestionVote', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(related_name=b'+', through='fugato.AnswerVote', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
