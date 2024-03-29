# reasoner.views
# Views for the reasoning prototype app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Jul 12 09:49:23 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the reasoning prototype app.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import viewsets
from users.mixins import LoginRequired
from django.views.generic import TemplateView

from reasoner.models import Dialogue, QuestionSeries
from reasoner.serializers import DialogueSerializer
from reasoner.serializers import DialogueCompleteSerializer
from reasoner.serializers import QuestionSeriesSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route

##########################################################################
## HTTP Generated Views
##########################################################################

class ReasonerPrototypeView(LoginRequired, TemplateView):

    template_name = "app/reasoner.html"

    def get_context_data(self, **kwargs):
        context = super(ReasonerPrototypeView, self).get_context_data(**kwargs)
        context['dialogue'] = Dialogue.objects.current(self.request.user, False)
        return context

##########################################################################
## API HTTP/JSON Views
##########################################################################

class DialogueViewSet(viewsets.ModelViewSet):

    queryset = Dialogue.objects.order_by('-started')
    serializer_class   = DialogueSerializer

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def graph(self, request, pk=None):
        instance = self.get_object()
        graph    = {'nodes':[], 'links':[]}
        nodemap  = {}

        for idx, qs in enumerate(instance.series.order_by('created')):
            nodemap[qs.question.pk] = idx
            graph['nodes'].append(
                {'name': str(qs.question), 'group': 1 if qs.is_subgoal else 2}
            )

            if qs.parent_goal:
                graph['links'].append(
                    {'source': nodemap[qs.question.pk], 'target': nodemap[qs.parent_goal.pk], 'value': 5}
                )

            if qs.previous:
                graph['links'].append(
                    {'source': nodemap[qs.previous.pk], 'target': nodemap[qs.question.pk], 'value': 1}
                )

        return Response(graph)

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        instance   = self.get_object()
        serializer = DialogueCompleteSerializer(
            data=request.DATA, context={'request': request}
        )

        if serializer.is_valid():

            for attr, value in serializer.validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            response = DialogueSerializer(instance, context={'request': request})
            return Response(response.data)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def questions(self, request, pk=None):

        return {
            'GET': self.questions_get,
            'POST': self.questions_post,
        }[request.method](request, pk)

    def questions_get(self, request, pk):
        """
        I hate this, I wish there was a better way of doing nested routing.
        This method returns a list of the dialogue questions.
        """
        instance   = self.get_object()
        serializer = QuestionSeriesSerializer(
            instance.series.all(), many=True, context={'request': request}
        )
        return Response(serializer.data)

    def questions_post(self, request, pk):
        """
        I hate this, I wish there was a better way of doing nested routing.
        This method creates a new question for the dialogue.
        """
        instance   = self.get_object()
        if instance.finished:
            return Response(
                {"success": False, "error": "session is finished"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = QuestionSeriesSerializer(
            data=request.DATA, context={'request': request, 'dialogue': instance}
        )

        if serializer.is_valid():
            # Save or update the QuestionSeries instance
            serializer.save()

            # Return the question data
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
