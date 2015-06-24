# kyudo.test_init
# Initialization tests for the Kyudo library
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 22 14:23:51 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: test_init.py [] bengfort@cs.umd.edu $

"""
Initialization tests for the Kyudo library
"""

##########################################################################
## Imports
##########################################################################

from unittest import TestCase

##########################################################################
## Module variables
##########################################################################

EXPECTED_VERSION = "1.1"

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

    def test_import(self):
        """
        Ensure the Kyudo module can be imported
        """
        try:
            import kyudo
        except ImportError:
            self.fail("Could not import the kyudo module.")

    def test_version(self):
        """
        Assert that test and package versions match
        """
        import kyudo
        self.assertEqual(EXPECTED_VERSION, kyudo.__version__)
