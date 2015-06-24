# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fugato', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freebase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicannotation',
            name='question',
            field=models.ForeignKey(related_name='annotations', to='fugato.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topicannotation',
            name='topic',
            field=models.ForeignKey(related_name='annotations', to='freebase.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topicannotation',
            name='user',
            field=models.ForeignKey(related_name='annotations', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
