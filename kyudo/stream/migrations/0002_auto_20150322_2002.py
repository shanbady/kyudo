# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamitem',
            name='verb',
            field=models.CharField(max_length=20, choices=[(b'join', b'joined'), (b'view', b'viewed'), (b'upvote', b'up voted'), (b'downvote', b'down voted'), (b'ask', b'asked'), (b'answer', b'answered'), (b'annotate', b'annotated')]),
            preserve_default=True,
        ),
    ]
