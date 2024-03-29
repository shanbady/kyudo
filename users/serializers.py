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

from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile

##########################################################################
## Serializers
##########################################################################


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes the Profile object to embed into the User JSON
    """

    gravatar = serializers.CharField(read_only=True)
    location = serializers.StringRelatedField()

    class Meta:
        model  = Profile
        fields = ('biography', 'gravatar', 'location', 'organization')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the User object for use in the API.
    """

    profile = ProfileSerializer(many=False, read_only=False)

    class Meta:
        model  = User
        fields = (
            'url', 'username', 'first_name',
            'last_name', 'email', 'profile'
        )
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail'}
        }

    def create(self, validated_data):
        """
        Explicitly define create to also create the Profile object.
        """
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)

        for attr, value in profile_data.items():
            setattr(user.profile, attr, value)

        user.profile.save()
        return user

    def update(self, instance, validated_data):
        """
        Explicitly define update to also update the Profile object.
        """
        profile_data = validated_data.pop('profile')
        profile      = instance.profile

        # Update the user instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the profile instance
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance


class SimpleUserSerializer(UserSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = (
            'url', 'username', 'full_name',
        )
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail'}
        }

    def get_full_name(self, obj):
        return obj.profile.full_name


class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200)
    repeated = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated']:
            raise serializers.ValidationError("passwords do not match!")
        return attrs


class LocationSerializer(serializers.Serializer):

    mid   = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=255, required=False)
