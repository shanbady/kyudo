# kyudo.settings.production
# The Django settings for Kyudo in Production
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Sep 12 16:16:44 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: production.py [] bengfort@cs.umd.edu $

"""
The Django settings for Kyudo in Production
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Production Settings
##########################################################################

## Debugging Settings
DEBUG            = False
TEMPLATE_DEBUG   = False

## Hosts
ALLOWED_HOSTS    = ['kyudo.bengfort.com', 'robinhood', '104.237.146.93']

## Static files served by Nginx
## Keep in mind also that Whitenoise is serving compressed assets
STATIC_ROOT = '/var/www/kyudo/static'
MEDIA_ROOT  = '/var/www/kyudo/media'

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
