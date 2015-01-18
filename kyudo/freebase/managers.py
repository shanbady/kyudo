# freebase.managers
# Custom managers for Freebase models
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Jan 18 08:43:54 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: managers.py [] bengfort@cs.umd.edu $

"""
Custom managers for Freebase models
"""

##########################################################################
## Imports
##########################################################################

from freebase.api import topic, summarize
from django.db import models, ProgrammingError

##########################################################################
## Topic Manager
##########################################################################

class TopicManager(models.Manager):

    def merge(self, mid):
        """
        Retrieves a Topic by mid, if doesn't exist, merges it from Freebase
        """

        # Strip the trailing slash
        if mid.endswith("/"):
            mid = mid.rstrip("/")

        results = self.filter(mid=mid)

        ## If result fetched from the database
        if len(results) == 1:
            return results[0]

        ## If no result fetched from the database
        if len(results) < 1:
            result  = topic(mid)
            summary = summarize(result)

            # Rename keys to fit the model
            summary['title'] = summary.pop('name')

            # Remove extra keys not required for model
            del summary['links']

            return self.create(**summary)

        ## If multiple results returned (shouldn't happen)
        if len(results) > 1:
            raise self.model.MultipleObjectsReturned()

        raise ProgrammingError("Merge operation should return or raise model (exception)")
