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
from fugato.models import Question
from rest_framework import serializers
from fugato.serializers import QuestionSerializer
from users.serializers import SimpleUserSerializer
from reasoner.models import Dialogue, QuestionSeries

##########################################################################
## Dialogue Serializer
##########################################################################


class DialogueSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize a dialogue object with additional information.
    """

    active    = serializers.SerializerMethodField()
    questions = serializers.StringRelatedField(many=True, read_only=True)
    user      = SimpleUserSerializer(
                    default=serializers.CurrentUserDefault(),
                    read_only=True,
                )

    class Meta:
        model = Dialogue
        extra_kwargs = {
            'url': {'view_name': 'api:dialogue-detail',},
        }

    def get_active(self, obj):
        return obj.active


##########################################################################
## Dialogue Management Serializers
##########################################################################


class DialogueCompleteSerializer(DialogueSerializer):
    """
    Simplified Dialogue serializer for managing dialogue complete states.
    """

    finished   = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model  = Dialogue
        fields = ('successful', 'completed', 'terminated', 'finished')


class DialogueQuestionSerializer(QuestionSerializer):
    """
    Overrides the create method so that the QuestionSerializer correctly
    handles duplicate questions as "GET OR CREATE" rather than returning an
    error to the front end.
    """

    author    = SimpleUserSerializer(
                    default=serializers.CurrentUserDefault(),
                    read_only=True,
                )
    related   = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model  = Question
        fields = ('url', 'text', 'author', 'page_url', 'related', 'details_rendered')
        extra_kwargs = {
            'url': {'view_name': 'api:question-detail',},
            'details_rendered': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Override the create method to deal with duplicate questions and
        other API-specific errors that can happen on Question creation.
        """
        return Question.objects.dedupe(**validated_data)


##########################################################################
## QuestionSeries Serializers
##########################################################################

class QuestionSeriesSerializer(serializers.ModelSerializer):

    question = DialogueQuestionSerializer()
    dialogue = serializers.HyperlinkedIdentityField(
                   read_only=True, view_name='api:dialogue-detail'
               )

    class Meta:
        model  = QuestionSeries
        fields = ('question', 'dialogue', 'is_subgoal', 'parent_goal')

    def create(self, validated_data):
        """
        Create the question, then create the question series instance.
        """
        question, _ = Question.objects.dedupe(**validated_data.pop("question"))
        validated_data['dialogue'] = self.context.get('dialogue', None)
        validated_data['question'] = question
        return super(QuestionSeriesSerializer, self).create(validated_data)
