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
from model_utils import Choices
from kyudo.utils import signature
from django.dispatch import receiver
from django.db.models.signals import pre_save
from model_utils.models import TimeStampedModel

##########################################################################
## Qustion and Answer Models
##########################################################################

class Question(TimeStampedModel):

    text     = models.CharField( max_length=512, null=False )  # The text of the question
    hash     = models.CharField( max_length=28, unique=True )  # The normalized signature
    related  = models.ManyToManyField( 'self' )                # Links between related questions
    author   = models.ForeignKey( 'auth.User', related_name="questions" )
    voters   = models.ManyToManyField( 'auth.User', through='fugato.QuestionVote', related_name="+")

    class Meta:
        db_table = "questions"
        get_latest_by = 'created'

    def __unicode__(self):
        return self.text

class Answer(TimeStampedModel):

    text     = models.TextField( )                             # The text of the answer
    related  = models.ManyToManyField( 'self' )                # Links between related responses
    author   = models.ForeignKey( 'auth.User', related_name="answers" )
    question = models.ForeignKey( 'fugato.Answer', related_name="answers" )
    voters   = models.ManyToManyField( 'auth.User', through='fugato.AnswerVote', related_name="+")

    class Meta:
        db_table = "answers"
        get_latest_by = 'created'

    def __unicode__(self):
        return self.text

##########################################################################
## Models for Up/Down voting
##########################################################################

class Voting(TimeStampedModel):
    """
    Abstract Voting model for up/down voting
    """

    BALLOT   = Choices((-1, 'downvote', 'downvote'), (1, 'upvote', 'upvote'), (0, 'novote', 'novote'))
    vote     = models.SmallIntegerField( choices=BALLOT, default=BALLOT.novote )

    class Meta:
        abstract = True
        get_latest_by = "modified"
        verbose_name  = "vote"
        verbose_name_plural = "votes"

class AnswerVote(Voting):

    answer   = models.ForeignKey( 'fugato.Answer', related_name='votes' )
    user     = models.ForeignKey( 'auth.User', related_name='answer_votes' )

    class Meta:
        db_table = "answer_voting"
        unique_together = ('answer', 'user')

class QuestionVote(Voting):

    question = models.ForeignKey( 'fugato.Question', related_name='votes' )
    user     = models.ForeignKey( 'auth.User', related_name='question_votes' )

    class Meta:
        db_table = "question_voting"
        unique_together = ('question', 'user')

##########################################################################
## Signals
##########################################################################

@receiver(pre_save, sender=Question)
def question_normalization(sender, instance, *args, **kwargs):
    instance.hash = signature(instance.text)
