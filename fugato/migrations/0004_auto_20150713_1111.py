# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fugato', '0003_parseannotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'text', unique=True, editable=False),
        ),
    ]
