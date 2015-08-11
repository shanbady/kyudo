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
from freebase.serializers import *
from rest_framework import viewsets
from users.mixins import LoginRequired
from users.permissions import IsAuthorOrReadOnly
from django.views.generic import DetailView, TemplateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route

## Similarity View Dependencies
from fugato.similarity import Similarity
from fugato.similarity import preselected_cases
from django.utils.six.moves import zip_longest

##########################################################################
## HTTP Generated Views
##########################################################################

class QuestionDetail(LoginRequired, DetailView):

    model = Question
    template_name = "fugato/question.html"
    context_object_name = "question"


class SimilarityView(LoginRequired, TemplateView):

    template_name = "fugato/similarity.html"

    def post(self, *args, **kwargs):
        """
        Handle question similarity data.
        """
        context = self.get_context_data()
        context['result'] = Similarity(context['cases'])
        return self.render_to_response(context)

    def parse_numcases(self):
        """
        Returns the number of cases from the GET query
        """
        arg = 2
        num = self.request.GET.get('numcases', arg)

        try:
            num = int(num)
            if num > 1:
                return num
        except ValueError:
            pass

        return arg

    def get_requested_cases(self):
        """
        Extract the requested cases from the POST data
        """
        empties   = lambda n: [""]*n
        numcases  = self.parse_numcases()

        ## Attempt to get questions from GET example
        if self.request.GET.get('example', None):
            slug = self.request.GET.get('example').lower()
            if slug in preselected_cases:
                return list(zip_longest(
                    preselected_cases[slug]['questions'],
                    preselected_cases[slug]['answers'],
                    fillvalue=""
                ))

        ## Attempt to get questions from POST data otherwise default to empties
        questions = self.request.POST.getlist('question', empties(numcases))
        answers   = self.request.POST.getlist('answer', empties(numcases))
        return list(zip_longest(questions, answers, fillvalue=""))

    def get_context_data(self, **kwargs):
        context = super(SimilarityView, self).get_context_data(**kwargs)
        context['cases']    = self.get_requested_cases()
        context['examples'] = preselected_cases.values()

        ## Handle case addtion and subtraction
        numcases = self.parse_numcases()
        context['addcase'] = numcases+1
        if numcases > 2:
            context['subcase'] = numcases-1
        return context


##########################################################################
## API HTTP/JSON Views
##########################################################################

class QuestionTypeaheadViewSet(viewsets.ViewSet):
    """
    Endpoint for returning a typeahead of question texts.
    """

    def list(self, request):
        queryset = Question.objects.values_list('text', flat=True)
        return Response(queryset)

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

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def annotations(self, request, pk=None):
        """
        Returns a list of all annotations associated with the question
        """
        question   = self.get_object()
        concepts   = question.annotations.order_by('-modified')
        page       = self.paginate_queryset(concepts)
        if page is not None:
            serializer = TopicAnnotationSerializer(page, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = TopicAnnotationSerializer(concepts, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def answers(self, request, pk=None):
        """
        Returns a list of all answers associated with the question
        """
        question   = self.get_object()
        answers    = question.answers.order_by('created') # TODO: order by vote count
        page       = self.paginate_queryset(answers)

        if page is not None:
            serializer = AnswerSerializer(page, context={'request': request})
            paginator  = self.pagination_class()
            return self.get_paginated_response(serializer.data)

        serializer = AnswerSerializer(answers, context={'request': request})
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):

    queryset = Answer.objects.order_by('-created')
    serializer_class = AnswerSerializer

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        Note that the upvotes and downvotes keys are required by the front-end
        """
        answer   = self.get_object()
        serializer = VotingSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():

            kwargs = {
                'content': answer,
                'user': request.user,
                'vote': serializer.validated_data['vote'],
            }

            _, created = Vote.objects.punch_ballot(**kwargs)
            response = serializer.data
            response.update({'status': 'vote recorded', 'created': created,
                             'upvotes': answer.votes.upvotes().count(),
                             'downvotes': answer.votes.downvotes().count()})
            return Response(response)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
