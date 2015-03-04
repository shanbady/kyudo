# freebase.views
# Views for the Freebase Application
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 04 18:53:21 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: views.py [] bengfort@cs.umd.edu $

"""
Views for the Freebase Application
"""

##########################################################################
## Imports
##########################################################################

import time

from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from freebase.models import *
from freebase.serializers import *
from freebase.api import search, topic, summarize
from freebase.nlp import entities, parse, extract_noun_phrases

##########################################################################
## API Views
##########################################################################

class TopicAnnotationViewSet(viewsets.ModelViewSet):
    """
    The standard viewset for the TopicAnnotation model.
    """

    queryset = TopicAnnotation.objects.order_by('-modified')
    serializer_class   = TopicAnnotationSerializer

##########################################################################
## Computed API ViewSets
##########################################################################

class ParserViewSet(viewsets.ViewSet):
    """
    Parses a sentence and ships it back
    """

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        query = request.GET.get('query', '')

        response = {
            'text': query
        }

        start = time.time()

        trees = parse(query)

        if len(trees) > 0:
            tree = trees[0]
            response['parse'] = tree.pprint()
            response['concepts'] = list(extract_noun_phrases(tree))
            response['entities'] = list(entities(query))
        else:
            response['parse'] = None
            response['concepts'] = []
            response['entities'] = []


        # Add the status
        response["time"] = time.time() - start

        if response['parse'] is not None:
            status = 'parsed in %0.4f seconds; extracted %i concepts and %i entities'
            status = status % (response['time'], len(response['concepts']), len(response['entities']))
        else:
            status = 'unable to parse input'

        response['status'] = status
        return Response(response)


class FreebaseViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    lookup_value_regex = '.+'

    def list(self, request):
        """
        Return a list of search results for a query
        """

        query = request.GET.get('query', None)
        if query is not None:
            response = search(query)
        else:
            response = []

        return Response(response)

    def retrieve(self, request, pk=None):
        """
        Returns a topic detail from Freebase for a particular mid
        """
        if pk is None:
            raise Http404

        if not pk.startswith("/"):
            pk = "/" + pk

        result = topic(pk)
        return Response(summarize(result))
