# fugato.serializers
# JSON Serializers for the Fugato app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Oct 23 15:03:36 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
JSON Serializers for the Fugato app
"""

##########################################################################
## Imports
##########################################################################

from fugato.models import *
from rest_framework import serializers

##########################################################################
## Serializers
##########################################################################

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    class Meta:
        model  = Question
        fields = ('id', 'text')

    def validate(self, attrs):
       """
       Check that the question hasn't already been asked.
       """
       if self.opts.model.objects.filter(hash=signature(attrs['text'])).exists():
            raise serializers.ValidationError("question has already been asked")
       return attrs
