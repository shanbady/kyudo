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
from kyudo.utils import signature
from django.dispatch import receiver
from django.db.models.signals import pre_save
from model_utils.models import TimeStampedModel

##########################################################################
## Models
##########################################################################

class Question(TimeStampedModel):

    text    = models.CharField( max_length=512, null=False )  # The text of the question
    hash    = models.CharField( max_length=28, unique=True )  # The normalized signature
    related = models.ManyToManyField( 'self' )                # Links between related questions
    users   = models.ManyToManyField( 'auth.User', related_name="questions")

    class Meta:
        db_table = "questions"

    def __unicode__(self):
        return self.text


##########################################################################
## Signals
##########################################################################

@receiver(pre_save, sender=Question)
def question_normalization(sender, instance, *args, **kwargs):
    instance.hash = signature(instance.text)
