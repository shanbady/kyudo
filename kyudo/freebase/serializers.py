# freebase.serializers
# API Serializers for the Freebase app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Jan 28 09:12:55 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: serializers.py [] bengfort@cs.umd.edu $

"""
API Serializers for the Freebase app
"""

##########################################################################
## Imports
##########################################################################

from freebase.models import *
from fugato.models import Question
from rest_framework import serializers
from rest_framework import pagination

##########################################################################
## TopicAnnotation Serializer
##########################################################################

class TopicAnnotationSerializer(serializers.ModelSerializer):

    user     = serializers.HyperlinkedRelatedField(
                default=serializers.CurrentUserDefault(),
                read_only=True,
                view_name="api:user-detail",
               )

    question = serializers.HyperlinkedRelatedField(
                view_name="api:question-detail",
                queryset=Question.objects.all(),
               )

    class Meta:
        model  = TopicAnnotation
        fields = ('user', 'question', 'text', 'topic')

class PaginatedTopicAnnotationSerializer(pagination.PaginationSerializer):
    """
    Paginates the TopicAnnotationSerializer
    """

    class Meta:
        object_serializer_class = TopicAnnotationSerializer
