# kyudo.wsgi
# WSGI Config for Kyudo project
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jun 23 09:42:10 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: wsgi.py [] benjamin@bengfort.com $

"""
WSGI config for kyudo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

##########################################################################
## Imports
##########################################################################

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

##########################################################################
## Configuration
##########################################################################

## Load settings from environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kyudo.settings.production")

## Create Whitenoise application
application = get_wsgi_application()
application = DjangoWhiteNoise(application)
