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
