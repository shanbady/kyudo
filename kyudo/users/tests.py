# users.tests
# Tests for the users app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 22 16:47:20 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.py [] bengfort@cs.umd.edu $

"""
Tests for the users app
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from users.models import Profile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

##########################################################################
## User Fixture
##########################################################################

fixtures = {
    'user': {
        'username': 'jdoe',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'supersecret',
    }
}

##########################################################################
## Model Tests
##########################################################################

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**fixtures['user'])

    def test_profile_on_create(self):
        """
        Test the User post_save signal to create a profile
        """

        self.assertEqual(Profile.objects.count(), 1, "begin profile count mismatch (user mock has no profile?)")
        u = User.objects.create_user(username="test", email="test@example.com", password="password")
        self.assertEqual(Profile.objects.count(), 2, "additional profile object doesn't exist")
        self.assertIsNotNone(u.profile)

    def test_profile_email_hash_md5(self):
        """
        Ensure that the email_hash on a user is an MD5 digest
        """

        email   = "Jane.Doe@gmail.com"
        udigest = hashlib.md5(email).hexdigest()
        ldigest = hashlib.md5(email.lower()).hexdigest()

        u = User.objects.create_user(username="test", email=email, password="password")
        self.assertIsNotNone(u.profile, "user has no profile?")
        self.assertIsNotNone(u.profile.email_hash, "user has no email hash?")

        self.assertNotEqual(udigest, u.profile.email_hash, "email was not lower case before digest")
        self.assertEqual(ldigest, u.profile.email_hash, "email not hashed correctly")

    def test_profile_email_hash_create(self):
        """
        Email should be hashed on user create
        """

        digest = hashlib.md5(fixtures['user']['email']).hexdigest()

        self.assertIsNotNone(self.user.profile, "user has no profile?")
        self.assertIsNotNone(self.user.profile.email_hash, "user has no email hash?")
        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")

    def test_profile_email_hash_update(self):
        """
        Email should be hashed on user update
        """

        newemail = "john.doe@gmail.com"
        digest   = hashlib.md5(newemail).hexdigest()

        self.user.email = newemail
        self.user.save()

        self.assertEqual(digest, self.user.profile.email_hash, "email hash does not match expected")

##########################################################################
## View Tests
##########################################################################

class UserViewsTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        self.client = Client()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout();

    def test_profile_view_auth(self):
        """
        Assert that profile can only be viewed if logged in.
        """
        endpoint = reverse('profile')
        loginurl = reverse('social:begin', args=('google-oauth2',))
        params   = "next=%s" % endpoint
        expected = "%s?%s" % (loginurl, params)
        response = self.client.get(endpoint)

        self.assertRedirects(response, expected, fetch_redirect_response=False)

    def test_profile_object(self):
        """
        Assert the profile gets the current user
        """

        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertEqual(self.user, response.context['user'])

    def test_profile_template(self):
        """
        Check that the right template is being used
        """
        endpoint = reverse('profile')

        self.login()
        response = self.client.get(endpoint)

        self.assertTemplateUsed(response, 'registration/profile.html')
