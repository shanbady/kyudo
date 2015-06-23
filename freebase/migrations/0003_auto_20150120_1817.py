# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('freebase', '0002_auto_20150115_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicannotation',
            name='topic',
            field=models.ForeignKey(related_name='annotations', default=None, blank=True, to='freebase.Topic', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topicannotation',
            name='user',
            field=models.ForeignKey(related_name='annotations', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
