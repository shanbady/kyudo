# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Question = apps.get_model("fugato", "Question")
    ParseAnnotation = apps.get_model("fugato", "ParseAnnotation")
    db_alias = schema_editor.connection.alias

    # Add a ParseAnnotation to every question
    for question in Question.objects.all():
        ParseAnnotation.objects.create(question=question)

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fugato', '0002_question_parse_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParseAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('correct', models.NullBooleanField()),
                ('question', models.OneToOneField(related_name='parse_annotation', to='fugato.Question')),
                ('user', models.ForeignKey(related_name='+', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'parse_annotations',
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            forwards_func,
        ),
    ]
