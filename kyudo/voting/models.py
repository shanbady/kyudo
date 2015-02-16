# voting.models
# ContentTypes based generic models for voting on anything!
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 15 16:02:31 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: models.py [] bengfort@cs.umd.edu $

"""
ContentTypes based generic models for voting on anything!
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from voting.managers import VotingManager

from stream.signals import stream

##########################################################################
## Models
##########################################################################

class Vote(TimeStampedModel):
    """
    Generic vote object for up and down voting things
    """

    BALLOT   = Choices((-1, 'downvote', 'downvote'), (1, 'upvote', 'upvote'), (0, 'novote', 'novote'))

    # Data fields for the voting object
    vote     = models.SmallIntegerField( choices=BALLOT, default=BALLOT.novote )
    user     = models.ForeignKey( 'auth.User', related_name='votes' )

    # Content types for a generic relationship (e.g. vote anything)
    content_type   = models.ForeignKey( ContentType )
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey( 'content_type', 'object_id' )

    # Set a custom manager for the Vote object
    objects   = VotingManager()

    def __unicode__(self):
        action = {
            -1: "down voted",
            0:  "no voted",
            1:  "up voted",
        }[self.vote]

        return u"%s %s %s" % (unicode(self.user), action, unicode(self.content_object))

    class Meta:
        db_table = "voting"
        get_latest_by = "modified"
        verbose_name  = "vote"
        verbose_name_plural = "votes"
        unique_together = ('object_id', 'user', 'content_type')

##########################################################################
## Signals
##########################################################################

@receiver(post_save, sender=Vote)
def send_voted_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "voted" activity to the stream on up/down vote

    Decisions:
        1. The vote object isn't included in the stream
        2. Activities are recorded even when votes are changed
        3. The target of the vote verb is the content_object
    """
    vote_verb = {
         1: 'upvote',
        -1: 'downvote',
         0:  None
    }[instance.vote]

    if vote_verb is None:
        return

    voted = {
        'sender':    sender,
        'actor':     instance.user,
        'verb':      vote_verb,
        'target':    instance.content_object,
    }
    stream.send(**voted)
