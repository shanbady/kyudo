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
