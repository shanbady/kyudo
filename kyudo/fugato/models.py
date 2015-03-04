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

import time

from django.db import models
from voting.models import Vote
from django.conf import settings
from stream.signals import stream
from autoslug import AutoSlugField
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from kyudo.utils import signature, nullable, htmlize
from django.contrib.contenttypes.fields import GenericRelation
from freebase.nlp import entities, parse, extract_noun_phrases, tree_from_string

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
    parse_time = models.FloatField( editable=False, **nullable )                  # The time it took to parse the question text
    related  = models.ManyToManyField( 'self', editable=False )                   # Links between related questions
    template = models.ForeignKey(                                                 # Question template for similarity
                'freebase.TextTemplate',
                related_name='questions',
                editable=False, **nullable
               )
    author   = models.ForeignKey( 'auth.User', related_name='questions' )         # The author of the question
    votes    = GenericRelation( Vote, related_query_name='questions' )            # Vote on whether or not the question is relevant
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

    def get_text_parse(self):
        """
        Returns a string of the parse tree and the time it took to parse
        """
        start = time.time()

        # Syntactic Parsing
        trees = parse(self.text)
        tree = trees[0].pprint() if len(trees) > 0 else None

        return (tree, time.time() - start)

    def get_text_concepts(self):
        """
        Returns a list of strings of extracted noun phrases and the time
        it took to perform the concept extraction.
        """

        # Cannot get concepts if there is no parse
        if not self.parse:
            return [], 0.0

        start = time.time()
        tree  = tree_from_string(self.parse)

        # Concepts Parsing
        concepts = []
        current  = set([annotation.text for annotation in self.annotations.all()])
        for concept in extract_noun_phrases(tree):
            if concept not in current:
                concepts.append(concept)

        return (concepts, time.time()-start)

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
    votes    = GenericRelation( Vote, related_query_name='answers' )             # Votes for the goodness of the answer

    class Meta:
        db_table = "answers"
        get_latest_by = 'created'

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:answer-detail', args=(self.pk,))

    def __unicode__(self):
        return self.text

##########################################################################
## Parse annotation model
##########################################################################

class ParseAnnotation(TimeStampedModel):
    """
    Helper model/table so that users can annotate if parses are correct
    """

    question = models.OneToOneField(                                            # The question being annotated
                'fugato.Question',
                related_name="parse_annotation"
               )
    user     = models.ForeignKey( 'auth.User', related_name='+', **nullable )   # The user doing the annotation
    correct  = models.NullBooleanField( )                                       # Whether or not the parse is correct

    def is_annotated(self):
        """
        Determines if the annotation has been marked
        """
        return self.correct is not None

    class Meta:
        db_table = "parse_annotations"
        get_latest_by = "created"

##########################################################################
## Question Signals
##########################################################################

@receiver(pre_save, sender=Question)
def question_normalization(sender, instance, *args, **kwargs):
    instance.hash = signature(instance.text)

@receiver(pre_save, sender=Question)
def question_render_markdown(sender, instance, *args, **kwargs):
    if instance.details == "":
        instance.details = None

    if instance.details is not None:
        instance.details_rendered = htmlize(instance.details)
    else:
        instance.details_rendered = None

@receiver(pre_save, sender=Question)
def parse_question(sender, instance, *args, **kwargs):
    if settings.STANFORD_PARSE_ON_SAVE:
        if not instance.parse:
            instance.parse, instance.parse_time = instance.get_text_parse()

@receiver(post_save, sender=Question)
def add_question_concepts(sender, instance, *args, **kwargs):
    if settings.STANFORD_PARSE_ON_SAVE:
        if not instance.annotations.exists():
            concepts, delta = instance.get_text_concepts()
            for concept in concepts:
                instance.annotations.create(text=concept)

@receiver(post_save, sender=Question)
def create_post_annotation(sender, instance, created, **kwargs):
    if created:
        ParseAnnotation.objects.create(question=instance, user=None, correct=None)

@receiver(post_save, sender=Question)
def send_asked_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "asked" activity to the stream on Question create
    """
    if created:
        joined = {
            'sender':    sender,
            'actor':     instance.author,
            'verb':      'ask',
            'target':    instance,
            'timestamp': instance.created,
        }
        stream.send(**joined)

##########################################################################
## Answer Signals
##########################################################################

@receiver(pre_save, sender=Answer)
def answer_render_markdown(sender, instance, *args, **kwargs):
    if instance.text is not None:
        instance.text_rendered = htmlize(instance.text)

@receiver(post_save, sender=Answer)
def send_answered_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "answered" activity to the stream on Question create
    """
    if created:
        activity = {
            'sender':    sender,
            'actor':     instance.author,
            'verb':      'answer',
            'theme':     instance,
            'target':    instance.question,
            'timestamp': instance.created,
        }
        stream.send(**activity)
