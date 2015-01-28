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
# from django.test import TestCase

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "1.0.3"

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
