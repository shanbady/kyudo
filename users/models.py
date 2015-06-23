# users.models
# Contains additional User profile data but no authentication
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 15 16:50:01 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: models.py [] bengfort@cs.umd.edu $

"""
Contains additional User profile data but no authentication
"""

##########################################################################
## Imports
##########################################################################

import urllib

from django.db import models
from kyudo.utils import nullable
from freebase.models import Topic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

##########################################################################
## UserProfile model
##########################################################################


class Profile(models.Model):

    user         = models.OneToOneField(User, editable=False)
    email_hash   = models.CharField(max_length=32, editable=False)
    biography    = models.CharField(max_length=255, **nullable)
    organization = models.CharField(max_length=255, **nullable)
    location     = models.ForeignKey('freebase.Topic', related_name="+",
                                     **nullable)

    def get_gravatar_url(self, size=200, default="mm"):
        """
        Computes the gravatar url from an email address
        """
        params = urllib.urlencode({'d': default, 's': str(size)})
        grvurl = "http://www.gravatar.com/avatar/%s?%s" % (self.email_hash,
                                                           params)
        return grvurl

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=24)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = "%s <%s>" % (self.full_name, self.user.email)
        return email.strip()

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:user-detail', args=(self.pk,))

    def set_location(self, mid):
        """
        Set the location topic on the user profile by mid
        """
        location = Topic.objects.merge(mid)
        self.location = location

    def __unicode__(self):
        return self.full_email
