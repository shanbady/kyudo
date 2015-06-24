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

##########################################################################
## Topic Field
##########################################################################

class TopicField(serializers.RelatedField):
    """
    The topic field handles the mid merge of a topic by default (similar
    to how a SlugField works) and provides a useful representation as well
    as fetching by merge.
    """

    default_error_messages = {
        'does_not_exist': 'Object with mid={value} does not exist.',
        'invalid': 'Invalid value, please pass a MID.',
    }

    def __init__(self, **kwargs):
        kwargs["allow_null"] = True
        super(serializers.RelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return Topic.objects.merge(data)
        except (TypeError, ValueError):
            self.fail(invalid)

    def to_representation(self, obj):
        return unicode(obj)

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

    topic    = TopicField()

    class Meta:
        model  = TopicAnnotation
        fields = ('url', 'user', 'question', 'text', 'topic')
        extra_kwargs = {
            'url': {'view_name': 'api:annotation-detail',}
        }
