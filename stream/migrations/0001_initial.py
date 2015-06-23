# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_object_id', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('theme_object_id', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('public', models.BooleanField(default=True)),
                ('verb', models.CharField(max_length=20, choices=[(b'view', b'viewed'), (b'upvote', b'up voted'), (b'downvote', b'down voted'), (b'ask', b'asked'), (b'answer', b'answered'), (b'annotate', b'annotated')])),
                ('details', models.TextField(default=None, null=True, blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('actor', models.ForeignKey(related_name='activity_stream', to=settings.AUTH_USER_MODEL)),
                ('target_content_type', models.ForeignKey(related_name='targets', default=None, blank=True, to='contenttypes.ContentType', null=True)),
                ('theme_content_type', models.ForeignKey(related_name='themes', default=None, blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-timestamp',),
                'db_table': 'activity_stream',
                'verbose_name': 'activity stream item',
                'verbose_name_plural': 'activity stream items',
            },
            bases=(models.Model,),
        ),
    ]
