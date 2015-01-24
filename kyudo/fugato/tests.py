# fugato.tests
# Tests the fugato app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Jan 23 07:27:20 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.py [] bengfort@cs.umd.edu $

"""
Tests the fugato app
"""

##########################################################################
## Imports
##########################################################################

from unittest import skip
from fugato.models import *
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

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
## Fugato models tests
##########################################################################

class ParseAnnotationModelTest(TestCase):

    def test_annotation_on_create(self):
        """
        Test the Question post_save signal to create a parse annotation
        """

        self.assertEqual(ParseAnnotation.objects.count(), 0, "begin profile count mismatch")

        text = "Can chickens fly?"
        user = User.objects.create_user(username="test", email="test@example.com", password="password")
        question = Question.objects.create(text=text, author=user)

        self.assertEqual(ParseAnnotation.objects.count(), 1, "parse annotation not created on question save")
        self.assertIsNotNone(question.parse_annotation)

class QuestionAPIViewSetTest(TestCase):

    def setUp(self):
        self.user   = User.objects.create_user(**fixtures['user'])
        fixtures['question']['author'] = self.user
        self.client = APIClient()

    def login(self):
        credentials = {
            'username': fixtures['user']['username'],
            'password': fixtures['user']['password'],
        }

        return self.client.login(**credentials)

    def logout(self):
        return self.client.logout();

    def test_question_list_auth(self):
        """
        Assert GET /api/question/ returns 403 when not logged in
        """
        endpoint = reverse('api:question-list')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_create_auth(self):
        """
        Assert POST /api/question/ returns 403 when not logged in
        """
        endpoint = reverse('api:question-list')
        response = self.client.post(endpoint, {'text': 'Where are my keys?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_retrieve_auth(self):
        """
        Assert GET /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_update_auth(self):
        """
        Assert PUT /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.put(endpoint, {'text': 'Why did the bear cross the road?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_delete_auth(self):
        """
        Assert DELETE /api/question/:id/ returns 403 when not logged in
        """
        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @skip("pending implementation")
    def test_question_parse_detail_auth(self):
        """
        Assert GET /api/question/:id/parse returns 403 when not logged in
        """
        pass

    @skip("pending implementation")
    def test_question_parse_update_auth(self):
        """
        Assert PUT /api/question/:id/parse returns 403 when not logged in
        """
        pass

    @skip("pending implementation")
    def test_question_list(self):
        """
        Test GET /api/question/ returns question list
        """
        self.login()

        endpoint = reverse('api:question-list')
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @skip("pending implementation")
    def test_question_create(self):
        """
        Test POST /api/question/ creates a question
        """
        self.login()

        endpoint = reverse('api:question-list')
        response = self.client.post(endpoint, {'text': 'Where are my keys?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @skip("pending implementation")
    def test_question_retrieve(self):
        """
        Test GET /api/question/:id/ returns a question detail
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @skip("pending implementation")
    def test_question_update(self):
        """
        Test PUT /api/question/:id/ updates a question
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.put(endpoint, {'text': 'Why did the bear cross the road?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_delete_auth(self):
        """
        Test DELETE /api/question/:id/ deletes a question
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url()
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse(Question.objects.filter(pk=question.pk).exists())

    def test_question_parse_detail(self):
        """
        Test GET /api/question/:id/parse returns a parse detail
        """

        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "parse/"

        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('question', response.data)
        self.assertIn('parse', response.data)
        self.assertIn('correct', response.data)
        self.assertIn('user', response.data)
        self.assertIsNone(response.data['correct'])

    def test_question_parse_update(self):
        """
        Test POST /api/question/:id/parse annotates the parse
        """
        self.login()

        question = Question.objects.create(**fixtures['question'])
        endpoint = question.get_api_detail_url() + "parse/"

        response = self.client.post(endpoint, {'correct': True}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'success': True}, response.data)

        result   = self.client.get(endpoint)
        self.assertIn('correct', result.data)
        self.assertTrue(result.data['correct'])
        self.assertTrue(Question.objects.get(pk=question.pk).parse_annotation.correct)

        response = self.client.post(endpoint, {'correct': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'success': True}, response.data)

        result   = self.client.get(endpoint)
        self.assertIn('correct', result.data)
        self.assertFalse(result.data['correct'])
        self.assertFalse(Question.objects.get(pk=question.pk).parse_annotation.correct)
