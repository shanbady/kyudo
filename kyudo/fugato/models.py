# fugato.models
# Models for the fugato app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Oct 23 14:05:24 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the fugato app.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from voting.models import Vote
from autoslug import AutoSlugField
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from kyudo.utils import signature, nullable, htmlize
from django.contrib.contenttypes.fields import GenericRelation

##########################################################################
## Qustion and Answer Models
##########################################################################

class Question(TimeStampedModel):

    text     = models.CharField( max_length=512, null=False )                     # The text of the question
    slug     = AutoSlugField( populate_from='text', unique=True )                 # The slug of the question
    hash     = models.CharField( max_length=28, unique=True, editable=False )     # The normalized signature
    details  = models.TextField( help_text="Edit in Markdown", **nullable )       # Additional details about the question
    details_rendered = models.TextField( editable=False, **nullable )             # HTML rendered details text from MD
    parse    = models.TextField( editable=False, **nullable )                     # The syntactic parse of the question text
    related  = models.ManyToManyField( 'self', editable=False )                   # Links between related questions
    template = models.ForeignKey(                                                 # Question template for similarity
                'freebase.TextTemplate',
                related_name='questions',
                editable=False, **nullable
               )
    author   = models.ForeignKey( 'auth.User', related_name='questions' )         # The author of the question
    votes    = GenericRelation( Vote, related_query_name='questions' )   # Vote on whether or not the question is relevant
    topics   = models.ManyToManyField(                                            # Extracted concepts from parse
                'freebase.Topic',
                related_name='questions',
                through='freebase.TopicAnnotation'
               )

    def get_absolute_url(self):
        """
        Return the detail view of the Question object
        """
        return reverse('question', kwargs={'slug': self.slug})

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:question-detail', args=(self.pk,))

    class Meta:
        db_table = "questions"
        get_latest_by = 'created'

    def __unicode__(self):
        return self.text

class Answer(TimeStampedModel):

    text     = models.TextField(                                                 # The text of the answer (markdown)
                null=False, blank=False,
                help_text="Edit in Markdown"
               )
    text_rendered = models.TextField( editable=False, null=False )               # HTML rendered details of the question
    related  = models.ManyToManyField( 'self' )                                  # Links between related responses
    author   = models.ForeignKey( 'auth.User', related_name="answers" )          # The author of the answer
    question = models.ForeignKey( 'fugato.Question', related_name="answers" )    # The question this answer answers
    votes    = GenericRelation( 'voting.Vote', related_query_name='answers' )    # Votes for the goodness of the answer

    class Meta:
        db_table = "answers"
        get_latest_by = 'created'

    def __unicode__(self):
        return self.text

##########################################################################
## Signals
##########################################################################

@receiver(pre_save, sender=Question)
def question_normalization(sender, instance, *args, **kwargs):
    instance.hash = signature(instance.text)

@receiver(pre_save, sender=Question)
def question_render_markdown(sender, instance, *args, **kwargs):
    if instance.details is not None:
        instance.details_rendered = htmlize(instance.details)

@receiver(pre_save, sender=Answer)
def answer_render_markdown(sender, instance, *args, **kwargs):
    if instance.text is not None:
        instance.text_rendered = htmlize(instance.text)
