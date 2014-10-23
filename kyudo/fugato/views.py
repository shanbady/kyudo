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
from rest_framework import viewsets

##########################################################################
## API HTTP/JSON Views
##########################################################################

class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.order_by('-created')
    serializer_class = QuestionSerializer
