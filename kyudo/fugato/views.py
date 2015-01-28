# fugato.views
# Views for the Fugato app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Oct 23 15:05:12 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the Fugato app
"""

##########################################################################
## Imports
##########################################################################

from fugato.models import *
from voting.models import Vote
from fugato.serializers import *
from voting.serializers import *
from django.views.generic import DetailView
from rest_framework import viewsets
from users.permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

##########################################################################
## HTTP Generated Views
##########################################################################

class QuestionDetail(DetailView):

    model = Question
    template_name = "app/question.html"
    context_object_name = "question"

##########################################################################
## API HTTP/JSON Views
##########################################################################

class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.order_by('-created')
    serializer_class   = QuestionSerializer

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def parse(self, request, pk=None):
        question = self.get_object()

        if request.method == 'GET':
            serializer = ParseAnnotationSerializer(question.parse_annotation, context={'request': request})
            return Response(serializer.data)

        else:
            serializer = ParseAnnotationSerializer(data=request.DATA, context={'request': request})
            if serializer.is_valid():
                # Set the annotator and correctness on the annotation
                question.parse_annotation.user = serializer.validated_data['user']
                question.parse_annotation.correct = serializer.validated_data['correct']
                question.parse_annotation.save()

                data = ParseAnnotationSerializer(question.parse_annotation, context={'request': request}).data
                data.update({'success': True})
                return Response(data)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        Note that the upvotes and downvotes keys are required by the front-end
        """
        question   = self.get_object()
        serializer = VotingSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'content': question,
                'user': request.user,
                'vote': serializer.validated_data['vote'],
            }

            _, created = Vote.objects.punch_ballot(**kwargs)
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created,
                             'upvotes': question.votes.upvotes().count(),
                             'downvotes': question.votes.downvotes().count()})
            return Response(response)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AnswerViewSet(viewsets.ModelViewSet):

    queryset = Answer.objects.order_by('-created')
    serializer_class = AnswerSerializer

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        answer   = self.get_object()
        serializer = VotingSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'answer': answer,
                'user': request.user,
                'defaults': {
                    'vote': serializer.data['vote'],
                }
            }

            _, created = AnswerVote.objects.update_or_create(**kwargs)
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created})
            return Response(response)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
