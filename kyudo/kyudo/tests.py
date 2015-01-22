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

from unittest import TestCase
# from django.test import TestCase

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "1.0.2"

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
