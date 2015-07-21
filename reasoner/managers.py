# reasoner.managers
# Managers for the Dialogue and other reasoner models.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jul 21 10:50:12 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Managers for the Dialogue and other reasoner models.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models

##########################################################################
## Dialogue Manager
##########################################################################

class DialogueManager(models.Manager):

    def current(self, user, active=True):
        """
        Returns the latest session of the user; and if active is True, then
        returns only a session that is active; otherwise returns the latest
        terminated/completed session. If there is no dialogue, returns None.
        """
        dialogue = self.filter(user=user).order_by('-started').first()
        if dialogue and active:
            if dialogue.active:
                return dialogue
            return None
        return dialogue
