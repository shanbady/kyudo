# users.serializers
# Serializers for the members models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun May 18 07:57:36 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializers for the members models
"""

##########################################################################
## Imports
##########################################################################

from users.models import *
from rest_framework import serializers
from rest_framework.compat import smart_text
from django.contrib.auth.models import User

##########################################################################
## Serializers
##########################################################################

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    class Meta:
        model  = User
        fields = ('id', 'username', 'first_name', 'last_name')

class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    repeated = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated']:
            raise serializers.ValidationError("passwords do not match!")
        return attrs
