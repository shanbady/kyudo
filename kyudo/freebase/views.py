from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from freebase.api import search, topic, summarize
from freebase.nlp import entities, parse, extract_noun_phrases

class ParserViewSet(viewsets.ViewSet):
    """
    Parses a sentence and ships it back
    """

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        query = request.GET.get('query', None)
        if not query:
            return Response([])

        response = {
            'text': query
        }

        tree = parse(query)[0]
        response['parse'] = tree.pprint()
        response['concepts'] = extract_noun_phrases(tree)
        response['entities'] = entities(query)

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
