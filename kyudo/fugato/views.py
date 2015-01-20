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
from fugato.serializers import *
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
    permission_classes = [IsAuthorOrReadOnly]

    def pre_save(self, obj):
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = self.request.user
        super(QuestionViewSet, self).pre_save(obj)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        question   = self.get_object()
        serializer = VotingSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'question': question,
                'user': request.user,
                'defaults': {
                    'vote': serializer.data['vote'],
                }
            }

            _, created = QuestionVote.objects.update_or_create(**kwargs)
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created})
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
