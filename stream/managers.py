# stream.managers
# Custom manager for stream item objects
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Feb 04 11:09:16 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: managers.py [] bengfort@cs.umd.edu $

"""
Custom manager for stream item objects
"""

##########################################################################
## Imports
##########################################################################

from django.db import models

##########################################################################
## StreamItem Manager
##########################################################################

class StreamItemManager(models.Manager):

    def user_stream(self, user, privacy=False):
        """
        Returns a queryset containing a specific user's feed. If privacy
        is set to True, then only returns public items for the user's feed.
        """
        queryset = self.filter(actor=user)
        if privacy:
            queryset = queryset.filter(public=True)

        return queryset.order_by('timestamp')
