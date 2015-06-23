# kyudo.settings.testing
# Testing settings to enable testing on Travis
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Sep 12 16:18:38 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: testing.py [] bengfort@cs.umd.edu $

"""
Testing settings to enable testing on Travis
"""

##########################################################################
## Imports
##########################################################################

import os
import tempfile

from .base import *

##########################################################################
## Testing Settings
##########################################################################

## Debugging Settings
DEBUG            = True
TEMPLATE_DEBUG   = True

## Hosts
ALLOWED_HOSTS    = ['localhost', '127.0.0.1']

## Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'kyudo'),
        'USER': environ_setting('DB_USER', 'postgres'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

STATICFILES_STORAGE =  'django.contrib.staticfiles.storage.StaticFilesStorage'

## Content with side effects
# MEDIA_ROOT       = tempfile.mkdtemp(suffix='media', prefix='kyudo')
# STATIC_ROOT      = tempfile.mkdtemp(suffix='static', prefix='kyudo')

## Content without? side effects
MEDIA_ROOT         = "/tmp/kyudo/media"
STATIC_ROOT        = "/tmp/kyudo/static"

##########################################################################
## Django REST Framework
##########################################################################

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
)

##########################################################################
## Stanford Paths
##########################################################################

## Add the JAVA_HOME
JAVA_HOME          = environ_setting("JAVA_HOME", "/usr/lib/jvm/java-8-oracle/")

## NER JAR and Models
STANFORD_NER_MODEL = "/usr/share/stanford/ner/classifiers/english.all.3class.distsim.crf.ser.gz"
STANFORD_NER_JAR   = "/usr/share/stanford/ner/stanford-ner-2014-01-04.jar"

## Parser JAR and Models
STANFORD_PARSER_MODELS = "/usr/share/stanford/parser/stanford-parser-3.5.0-models.jar"
STANFORD_PARSER_JAR    = "/usr/share/stanford/parser/stanford-parser.jar"

## Stanford NLP not yet configured
STANFORD_PARSE_ON_SAVE = False
