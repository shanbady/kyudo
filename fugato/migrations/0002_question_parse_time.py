# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fugato', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='parse_time',
            field=models.FloatField(default=None, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
