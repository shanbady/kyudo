# voting.tests
# Tests for the voting module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jan 27 08:49:03 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.py [] bengfort@cs.umd.edu $

"""
Tests for the voting module
"""

##########################################################################
## Imports
##########################################################################

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import serializers

from fugato.models import *
from voting.models import *
from voting.serializers import *
from django.contrib.auth.models import User

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
    }
}

##########################################################################
## Serializer Tests
##########################################################################

class SerializerTests(APITestCase):
    """
    Test added functionality in voting serializers
    """

    def assertNotRaises(self, exc, fun, *args, **kwds):
        try:
            fun(*args, **kwds)
        except exc:
            self.fail("%s exception was raised", exc.__class__.__name__)

    def test_in_range_validator(self):
        """
        Test the in-range validator
        """

        validator = InRange(-1, 1)

        self.assertRaises(serializers.ValidationError, validator, -2)
        self.assertRaises(serializers.ValidationError, validator, 2)
        self.assertNotRaises(serializers.ValidationError, validator, -1)
        self.assertNotRaises(serializers.ValidationError, validator, 1)
        self.assertNotRaises(serializers.ValidationError, validator, 0)

    def test_voting_serializer_vote_range(self):
        """
        Ensure that the vote in the serializer is in range
        """

        serializer = VotingSerializer(data={"vote":-1})
        self.assertTrue(serializer.is_valid(), "downvote is not valid")

        serializer = VotingSerializer(data={"vote":0})
        self.assertTrue(serializer.is_valid(), "novote is not valid")

        serializer = VotingSerializer(data={"vote":1})
        self.assertTrue(serializer.is_valid(), "upvote is not valid")

        serializer = VotingSerializer(data={"vote":10})
        self.assertFalse(serializer.is_valid(), "bad vote is valid")

##########################################################################
## Model Tests
##########################################################################

class VotingModelTests(TestCase):
    """
    Test the Vote model/manager functionality
    """

    def setUp(self):
        self.user     = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user
        self.question = Question.objects.create(**fixtures['question'])

    def test_punch_ballot(self):
        """
        Test the punch ballot method of the Vote manager
        """

        # Ensure that there are no votes for the question to start
        self.assertEqual(self.question.votes.count(), 0)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        vote, created = Vote.objects.punch_ballot(self.question, self.user, 1)
        self.assertTrue(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 1)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        vote, created = Vote.objects.punch_ballot(self.question, self.user, -1)
        self.assertFalse(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 1)

        vote, created = Vote.objects.punch_ballot(self.question, self.user)
        self.assertFalse(created)
        self.assertEqual(self.question.votes.count(), 1)
        self.assertEqual(Vote.objects.upvotes().count(), 0)
        self.assertEqual(Vote.objects.downvotes().count(), 0)

        self.assertEqual(Vote.objects.count(), 1)


    def test_punch_ballot_kwargs(self):
        """
        Ensure that punch ballot requires content and user
        """
        self.assertRaises(TypeError, Vote.objects.punch_ballot, content=self.question)
        self.assertRaises(TypeError, Vote.objects.punch_ballot, user=self.user)

