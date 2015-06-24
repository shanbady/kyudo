# kyudo.settings.development
# The Django settings for Kyudo in development
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Sep 12 16:15:24 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: development.py [] bengfort@cs.umd.edu $

"""
The Django settings for Kyudo in development
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Development Settings
##########################################################################

## Debugging Settings
DEBUG            = True
TEMPLATE_DEBUG   = True

## Hosts
ALLOWED_HOSTS    = ('127.0.0.1', 'localhost')

## Secret Key doesn't matter in Dev
SECRET_KEY = 'cyt*c1@%sg6j@g6y9fdrd@iakg7)ek!dqb@7grl(c-nkm%2596'

## Content
MEDIA_ROOT       = os.path.join(PROJECT, 'media')
STATIC_ROOT      = os.path.join(PROJECT, 'static')

##########################################################################
## Django REST Framework
##########################################################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 200,
}

##########################################################################
## Stanford Paths
##########################################################################

## NER JAR and Models
STANFORD_NER_MODEL = os.path.expanduser("~/Development/stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz")
STANFORD_NER_JAR   = os.path.expanduser("~/Development/stanford-ner-2014-01-04/stanford-ner-2014-01-04.jar")

## Parser JAR and Models
STANFORD_PARSER_MODELS = os.path.expanduser("~/Development/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar")
STANFORD_PARSER_JAR    = os.path.expanduser("~/Development/stanford-parser-full-2014-10-31/stanford-parser.jar")
