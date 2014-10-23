# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('text', models.CharField(max_length=512)),
                ('hash', models.CharField(unique=True, max_length=28)),
                ('related', models.ManyToManyField(related_name='related_rel_+', to='fugato.Question')),
                ('users', models.ManyToManyField(related_name=b'questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'questions',
            },
            bases=(models.Model,),
        ),
    ]
