# freebase.signals
# Signals for the freebase app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 15:40:33 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: signals.py [] bengfort@cs.umd.edu $

"""
Signals for the freebase app
"""

##########################################################################
## Imports
##########################################################################

from stream.signals import stream
from django.dispatch import receiver
from django.db.models.signals import post_save

from freebase.models import TopicAnnotation

##########################################################################
## Signals
##########################################################################

@receiver(post_save, sender=TopicAnnotation)
def send_annotation_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "annotated" activity to the stream on Annotation create or update
    """

    # If no user, this is a parse annotation
    if instance.user is None:
        return

    activity = {
        'sender':    sender,
        'actor':     instance.user,
        'verb':      'annotate',
        'target':    instance.question,

        'timestamp': instance.modified,
    }

    # Topic can be null
    if instance.topic:
        activity['theme'] = instance.topic

    stream.send(**activity)
