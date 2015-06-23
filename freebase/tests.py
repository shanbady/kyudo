# freebase.tests
# Tests for the freebase app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 15:48:13 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.py [] bengfort@cs.umd.edu $

"""
Tests for the freebase app
"""

##########################################################################
## Imports
##########################################################################

from unittest import skip
from django.test import TestCase

from stream.signals import stream
from stream.models import StreamItem

from fugato.models import Question
from django.contrib.auth.models import User
from freebase.models import Topic, TopicAnnotation
from freebase.serializers import TopicAnnotationSerializer
from django.contrib.contenttypes.models import ContentType

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

##########################################################################
## Fixtures
##########################################################################

fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    },
    'question': {
        'text': 'Why did the chicken cross the road?',
        'author': None
    },
    'answer': {
        'question': None,
        'author': None,
        'text': 'To get to the other side.',
    },
    'topic': {
        "mid": "/m/060d2",
        "title": "President of the United States",
        "notability": "Government Office or Title",
        "image": "https://usercontent.googleapis.com/freebase/v1/image/m/02fx33v?maxheight=225&maxwidth=225",
        "description": "The President of the United States of America (acronym: POTUS) is the head of state and head of government of the United States. The president leads the executive branch of the federal government and is the commander-in-chief of the United States Armed Forces."
    },
    'annotation': {
        'text': 'chicken',
        'user': None,
        'question': None,
        'topic': None
    }
}

##########################################################################
## Manager Tests
##########################################################################

class TopicManagerTests(TestCase):

    @skip("pending implementation")
    def test_mid_strip_slash(self):
        """
        Ensure that trailing slashes are stripped from MID
        """
        pass

    @skip("pending implementation")
    def test_merge_model_fetch(self):
        """
        Ensure that models are fetched from Freebase on no lookup
        """
        pass

    @skip("pending implementation")
    def test_merge_model(self):
        """
        Ensure that models are fetched from database if they exist
        """
        pass

##########################################################################
## Serializer Tests
##########################################################################

class FreebaseSerializerTests(TestCase):

    @skip("pending implementation")
    def test_topic_field(self):
        """
        Ensure that the topic field representation and merge works
        """
        pass

    @skip("pending implementation")
    def test_topic_annotation_serializer(self):
        """
        Test the default user, topic field, and other serializer details
        """
        pass

    @skip("pending implementation")
    def test_topic_annotation_serializer_url(self):
        """
        Assert the URL is correctly found with the view_name kwarg
        """
        pass

    @skip("pending implementation")
    def test_paginated_topic_annotation_serializer(self):
        """
        Test pagination with the topic annotation serializer
        """
        pass

##########################################################################
## API Tests
##########################################################################

class FreebaseAPIViewsTests(TestCase):

    @skip("pending implementation")
    def test_topic_annotation_update(self):
        """
        Ensure topic annotation can be updated with an mid
        """
        pass

    @skip("pending implementation")
    def test_topic_annotation_update_error(self):
        """
        Test bad MID passed to topic annotation update
        """
        pass

    @skip("pending implementation")
    def test_topic_anntation_update_current_user(self):
        """
        Assert that the current user is marked in annotation
        """
        pass

##########################################################################
## Model tests
##########################################################################

class FreebaseModelTests(TestCase):

    def setUp(self):
        self.user     = User.objects.create_user(**fixtures['user'])
        self.topic    = Topic.objects.create(**fixtures['topic'])
        fixtures['question']['author'] = self.user

        self.question = Question.objects.create(**fixtures['question'])
        fixtures['annotation']['user']     = self.user
        fixtures['annotation']['topic']    = self.topic
        fixtures['annotation']['question'] = self.question

    def test_topic_annotation_send_stream(self):
        """
        Assert that when a TopicAnnotation is created it sends a stream signal
        """

        handler = MagicMock()
        stream.connect(handler)
        annotation = TopicAnnotation.objects.create(**fixtures['annotation'])

        # Ensure that the signal was sent once with required arguments
        handler.assert_called_once_with(verb='annotate', sender=TopicAnnotation,
                    timestamp=annotation.modified, actor=self.user,
                    target=self.question, signal=stream, theme=self.topic)

    @skip("pending implementation")
    def test_topic_annotation_update_send_stream(self):
        """
        Assert that when a TopicAnnotation is updated it sends a stream signal
        """
        pass

    def test_topic_annotation_activity_stream(self):
        """
        Test that annotation causes an activity stream item
        """

        annotation = TopicAnnotation.objects.create(**fixtures['annotation'])
        target_content_type = ContentType.objects.get_for_model(self.question)
        target_object_id    =  self.question.id
        theme_content_type  = ContentType.objects.get_for_model(self.topic)
        theme_object_id     = self.topic.id

        query = StreamItem.objects.filter(verb='annotate', actor=self.user,
                    target_content_type=target_content_type, target_object_id=target_object_id,
                    theme_content_type=theme_content_type, theme_object_id=theme_object_id)
        self.assertEqual(query.count(), 1, "no stream item created!")

    @skip("pending implementation")
    def test_ta_activity_stream_from_parse(self):
        """
        Assert no stream item is created when a user isn't involved
        """
        pass

    @skip("pending implementation")
    def test_ta_stream_null_topic(self):
        """
        Assert an activity stream is created even on no topic
        """
        pass
