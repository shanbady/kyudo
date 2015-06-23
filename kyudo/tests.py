# kyudo.tests
# Tests for the Kyudo library
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 22 14:23:51 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.py [] bengfort@cs.umd.edu $

"""
Tests for the Kyudo library
"""

##########################################################################
## Imports
##########################################################################

import kyudo

from kyudo.utils import *
from unittest import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "1.0.4"

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTests(TestCase):
    """
    Some basic Kyudo tests
    """

    def test_sanity(self):
        """
        Check that the world is sane and 2+2=4
        """
        self.assertEqual(2+2, 4)

    def test_version(self):
        """
        Assert that test and package versions match
        """
        self.assertEqual(EXPECTED_VERSION, kyudo.get_version())

class UtilsTests(TestCase):
    """
    Test the kyudo utilities library
    """

    def test_normalize(self):
        """
        Test the normalization function
        """

        self.assertNotIn(" ", normalize("a b c d e f     g"), "should not contain spaces")
        self.assertNotIn("A", normalize("AAAAA AAA AA 9AA8"), "should not contain uppercase")
        self.assertNotIn(".", normalize("no.punctuation."), "should not contain punctuation")
        self.assertNotIn("-", normalize("no-punctuation-"), "should not contain punctuation")

    def test_normalize_question(self):
        """
        Test question normalization
        """

        testa = "Who is faster, a T-Rex or a Velociraptor?"
        testb = "who is faster? A t-rex or a velociraptor?"

        self.assertEqual(normalize(testa), normalize(testb))

    def test_signature(self):
        """
        Test the text signature method
        """

        self.assertEqual(len(signature("here I am")), 28, "should be base64 encoded SHA1 hash length")
        self.assertEqual(signature("the rain in spain"), "QKv9wgxE3wSgRQevr3h1S0cg468=", "should compute the correct SHA1 hash")

    def test_question_signature(self):
        """
        Test questions with same signature
        """

        testa = "Who is faster, a T-Rex or a Velociraptor?"
        testb = "who is faster? A t-rex or a velociraptor?"

        self.assertEqual(signature(testa), signature(testb))

    def test_htmlize(self):
        """
        Test the htmlize function
        """

        self.assertEqual(htmlize("http://www.google.com/"), '<p><a href="http://www.google.com/" rel="nofollow">http://www.google.com/</a></p>', "linkify didn't work")
        self.assertNotIn("<script>", htmlize("<script>alert('bad');</script>"), "clean didn't work")
        self.assertIn("<ul>", htmlize("- item 1\n- item 2\n"), "markdown didn't work")

##########################################################################
## API Tests
##########################################################################

class APITests(APITestCase):
    """
    Check the default APIs like the heartbeat endpoint
    """

    def setUp(self):
        self.endpoint = url = reverse('api:status-list')

    def test_heartbeat_no_auth(self):
        """
        Assert that the heartbeat endpoint requires no auth
        """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_heartbeat_get_only(self):
        """
        Assert that the heartbeat endpoint is GET only
        """
        data = {"name": "Rebbecca", "color": "red"}

        # Test POST
        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PUT
        response = self.client.put(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test DELETE
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_heartbeat(self):
        """
        Check the heartbeat endpoint for content
        """
        expected = {'status': 'ok', 'version': EXPECTED_VERSION}
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('timestamp', response.data)
        ts = response.data.pop('timestamp')
        self.assertEqual(expected, response.data)

