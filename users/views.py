# users.views
# Views for users and contributor management
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri May 16 15:38:56 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for users and contributor management
"""

##########################################################################
## Imports
##########################################################################

from users.mixins import LoginRequired
from users.permissions import IsAdminOrSelf
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from users.serializers import LocationSerializer
from users.serializers import UserSerializer, PasswordSerializer

##########################################################################
## Views
##########################################################################


class ProfileView(LoginRequired, TemplateView):
    """
    A simple template view to display a reviewer's profile including their
    upvoting and down voting statistics.
    """

    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        """
        Computes the gravatar from the user email and adds data to the
        context to render the template.
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        stream = self.request.user.activity_stream.all()[:10]
        context['activity_stream'] = stream

        return context

##########################################################################
## API HTTP/JSON Views
##########################################################################


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'], permission_classes=[IsAdminOrSelf])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.DATA)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], permission_classes=[IsAdminOrSelf])
    def set_location(self, request, pk=None):
        user = self.get_object()
        serializer = LocationSerializer(data=request.DATA)
        if serializer.is_valid():
            user.profile.set_location(serializer.data['mid'])
            user.profile.save()

            location_serializer = LocationSerializer(user.profile.location)
            return Response({
                'status': 'location set',
                'location': location_serializer.data
            })

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
