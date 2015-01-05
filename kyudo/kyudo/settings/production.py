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
ALLOWED_HOSTS    = ['localhost', '127.0.0.1']

## Static files served by Nginx
STATIC_ROOT = '/var/www/kyudo/static'
MEDIA_ROOT  = '/var/www/kyudo/media'

##########################################################################
## Stanford Paths
##########################################################################

## NER JAR and Models
STANFORD_NER_MODEL = "/var/lib/stanford/stanford-ner-2014-01-04/classifiers/english.all.3class.distsim.crf.ser.gz"
STANFORD_NER_JAR   = "/var/lib/stanford/stanford-ner-2014-01-04/stanford-ner-2014-01-04.jar"

## Parser JAR and Models
STANFORD_PARSER_MODELS = "/var/lib/stanford/stanford-parser-full-2014-10-31/stanford-parser-3.5.0-models.jar"
STANFORD_PARSER_JAR    = "/var/lib/stanford/stanford-parser-full-2014-10-31/stanford-parser.jar"
