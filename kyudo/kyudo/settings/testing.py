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
        'PASSWORD': 'tr4v1sT3ST3R!',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
