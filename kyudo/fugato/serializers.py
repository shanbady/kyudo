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
        fields = ('id', 'text', 'author', 'created', 'modified')
        read_only_fields = ('author',)

    def validate(self, attrs):
       """
       Check that the question hasn't already been asked.
       """
       if self.opts.model.objects.filter(hash=signature(attrs['text'])).exists():
            raise serializers.ValidationError("question has already been asked")
       return attrs

class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializes the Answer object for use in the API.
    """

    class Meta:
        model  = Answer
        fields = ('id', 'text', 'author', 'question', 'created', 'modified')
        read_only_fields = ('author', 'question', 'created', 'modified')

class VotingSerializer(serializers.Serializer):
    """
    Serializes incoming votes.
    """

    vote    = serializers.IntegerField()
    display = serializers.SerializerMethodField('get_vote_display')

    def validate_vote(self, attrs, source):
        value = attrs[source]
        if value > 1 or value < -1:
            raise serializers.ValidationError("vote must be between -1 and 1")
        return attrs

    def get_vote_display(self, obj):
        displays = {
            -1: "downvote",
             0: "novote",
             1: "upvote",
        }

        return displays[obj['vote']]
