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
from freebase.managers import TopicManager
from django.core.urlresolvers import reverse
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


    ## Set a custom manager on the topics
    objects     = TopicManager()


    class Meta:
        db_table = "topics"

    def __unicode__(self):
        return self.title

class TopicAnnotation(TimeStampedModel):

    text     = models.CharField( max_length=255 ) # The text that's being annotated with a topic
    topic    = models.ForeignKey( 'freebase.Topic', related_name='annotations', **nullable )
    question = models.ForeignKey( 'fugato.Question', related_name='annotations' )
    user     = models.ForeignKey( 'auth.User', related_name='annotations', **nullable )

    class Meta:
        db_table = "annotations"
        get_latest_by = "created"

    def is_ambiguous(self):
        """
        Decides if the annotation is ambiguous or not
        """
        return self.topic is None

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:annotation-detail', args=(self.pk,))

    def __unicode__(self):
        if self.topic:
            return unicode(self.topic)
        else:
            return self.text
