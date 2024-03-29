# fugato.managers
# Custom managers for the fugato models
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Jul 22 14:03:52 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: managers.py [] benjamin@bengfort.com $

"""
Custom managers for the fugato models
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from kyudo.utils import signature

##########################################################################
## Questions Manager
##########################################################################

class QuestionManager(models.Manager):

    def dedupe(self, raise_for_exceptions=False, **kwargs):
        """
        Essentially a GET or CREATE method that checks if a duplicate
        question already exists in the database by its hash. If
        raise_for_exceptions is True, then will raise a DuplicateQuestion
        exception, otherwise it will return None.

        Returns question, created where created is a Boolean
        """
        hash  = signature(kwargs['text'])
        query = self.filter(hash=hash)
        if query.exists():
            if raise_for_exceptions:
                raise DuplicateQuestion()
            return query.first(), False

        return self.create(**kwargs), True
