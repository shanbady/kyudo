from unittest import skip
from django.test import TestCase

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
    def test_paginated_topic_annotation_serializer(self):
        """
        Test pagination with the topic annotation serializer
        """
        pass

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

class FreebaseModelTests(TestCase):

    @skip("pending implementation")
    def test_topic_annotation_activity_stream(self):
        """
        Test that annotation causes an activity stream item
        """
        pass

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
