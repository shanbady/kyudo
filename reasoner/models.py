# reasoner.models
# Models for the reasoner app.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Jul 12 10:24:29 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the reasoner app.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from datetime import datetime
from kyudo.utils import nullable
from django.core.urlresolvers import reverse
from reasoner.managers import DialogueManager
from reasoner.managers import QuestionSeriesManager
from model_utils.models import TimeStampedModel

##########################################################################
## Session Models
##########################################################################

class Dialogue(models.Model):

    user       = models.ForeignKey('auth.User', related_name="dialogues")
    started    = models.DateTimeField(auto_now_add=True)
    finished   = models.DateTimeField(**nullable)
    modified   = models.DateTimeField(auto_now=True)
    successful = models.NullBooleanField(default=None, help_text="the dialog was successful")
    completed  = models.BooleanField(default=False, help_text="user has finished the dialog")
    terminated = models.BooleanField(default=False, help_text="dialog closed after inactivity")
    questions  = models.ManyToManyField(
                    'fugato.Question', related_name='dialogues',
                    through="QuestionSeries", through_fields=('dialogue', 'question')
                )

    ## Custom manager object
    objects    = DialogueManager()

    @property
    def active(self):
        """
        Computes whether or not the current dialogue is active.
        """
        return (
            not self.completed and not self.terminated
        )

    def subgoals(self):
        return self.questions.through.objects.subgoals()

    def duration(self, struct=False):
        """
        Returns the number of seconds the dialoge lasted, or the current
        duration if the session has not been completed yet. This method is
        also used for determining whether or not the dialogue should be
        terminated (e.g. timed out).

        If struct is True - this returns a timedelta object rather than
        seconds integer.
        """
        tstamp = self.finished if self.finished else datetime.now()
        delta  = tstamp - self.started

        if struct:
            return delta
        return delta.total_seconds()

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:dialogue-detail', args=(self.pk,))

    class Meta:
        db_table = "dialogues"
        get_latest_by = 'started'


class QuestionSeries(TimeStampedModel):

    # M2M relationship
    question    = models.ForeignKey('fugato.Question', related_name="series")
    dialogue    = models.ForeignKey('Dialogue', related_name="series")

    # Tracks timeline of question answering
    previous    = models.ForeignKey('fugato.Question', related_name="followups", **nullable)

    # Tracks goal hierarchy of dialogue
    is_subgoal  = models.BooleanField(default=False)
    parent_goal = models.ForeignKey('fugato.Question', related_name="child_goals", **nullable)

    ## Custom manager object
    objects     = QuestionSeriesManager()

    class Meta:
        db_table = "dialogue_question_series"
        get_latest_by = 'created'
