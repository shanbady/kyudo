# freebase.models
# Models for storing RDF Topics
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 15 11:28:02 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: models.py [] bengfort@cs.umd.edu $

"""
Models for storing RDF Topics
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from jsonfield import JSONField
from kyudo.utils import nullable
from model_utils.models import TimeStampedModel

##########################################################################
## Models
##########################################################################

class TextTemplate(models.Model):
    pass

    class Meta:
        db_table = "templates"

class Topic(models.Model):

    mid         = models.CharField( max_length=32, unique=True ) # The mid from Freebase
    title       = models.CharField( max_length=512 )             # The title of the topic (or name in Freebase)
    notability  = models.CharField( max_length=512, **nullable)  # The reason or importance of the topic
    image       = models.URLField( max_length=2000, **nullable ) # A link to the image of the Topic
    attrs       = JSONField( **nullable )                        # A JSON list of arbitrary attributes
    description = models.TextField( **nullable )                 # A textual description of the topic

    class Meta:
        db_table = "topics"

    def __unicode__(self):
        return self.title

class TopicAnnotation(TimeStampedModel):

    text     = models.CharField( max_length=255 ) # The text that's being annotated with a topic
    topic    = models.ForeignKey( 'freebase.Topic', related_name='annotations' )
    question = models.ForeignKey( 'fugato.Question', related_name='annotations' )
    user     = models.ForeignKey( 'auth.User', related_name='annotations' )

    class Meta:
        db_table = "annotations"
        get_latest_by = "created"
