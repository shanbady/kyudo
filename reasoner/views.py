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

from reasoner.models import Dialogue
from reasoner.serializers import DialogueSerializer
from reasoner.serializers import DialogueCompleteSerializer

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

            response = DialogueSerializer(instance).data
            return Response(response)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
