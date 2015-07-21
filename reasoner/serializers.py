# reasoner.serializers
# API Serializers for the Reasoner app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jul 21 11:12:24 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
API Serializers for the Reasoner app
"""

##########################################################################
## Imports
##########################################################################

from django.utils import timezone
from reasoner.models import Dialogue
from rest_framework import serializers

##########################################################################
## Dialogue Serializer
##########################################################################

class DialogueSerializer(serializers.ModelSerializer):

    active    = serializers.SerializerMethodField()

    class Meta:
        model = Dialogue

    def get_active(self, obj):
        return obj.active

class DialogueCompleteSerializer(serializers.Serializer):

    successful = serializers.NullBooleanField(default=None)
    completed  = serializers.BooleanField(default=False)
    terminated = serializers.BooleanField(default=False)
    finished   = serializers.DateTimeField(default=timezone.now)
