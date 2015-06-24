# kyudo.tests.test_api
# Testing the root api components that aren't part of an app.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jun 23 11:56:31 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: test_api.py [] benjamin@bengfort.com $

"""
Testing the root api components that aren't part of an app.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from kyudo.tests.test_init import EXPECTED_VERSION

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
