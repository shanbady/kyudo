# users.signals
# Signals management for the Users app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 23:30:27 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: signals.py [] bengfort@cs.umd.edu $

"""
Signals management for the Users app
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from stream.signals import stream
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import Profile
from django.contrib.auth.models import User

##########################################################################
## Signals
##########################################################################

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    digest = hashlib.md5(instance.email.lower()).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()

@receiver(post_save, sender=User)
def send_joined_activity_signal(sender, instance, created, **kwargs):
    """
    Sends the "joined" activity to the stream on create
    """
    if created:
        joined = {
            'sender':    sender,
            'actor':     instance,
            'verb':      'join',
            'timestamp': instance.date_joined,
        }
        stream.send(**joined)
