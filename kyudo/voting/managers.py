# voting.managers
# Custom manager model for voting objects
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jan 20 12:42:19 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: managers.py [] bengfort@cs.umd.edu $

"""
Custom manager model for voting objects
"""

##########################################################################
## Imports
##########################################################################

from django.db import models

##########################################################################
## Voting Manager
##########################################################################

class VotingManager(models.Manager):

    def upvotes(self):
        """
        Return only the upvoted
        """
        return self.filter(vote=self.model.BALLOT.upvote)

    def downvotes(self):
        """
        Return only the down votes
        """
        return self.filter(vote=self.model.BALLOT.downvote)
