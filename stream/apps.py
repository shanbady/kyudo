# stream.apps
# Describes the Stream application for Django
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 23:25:07 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: apps.py [] bengfort@cs.umd.edu $

"""
Describes the Stream application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Freebase Config
##########################################################################

class StreamConfig(AppConfig):
    name = 'stream'
    verbose_name = "Activity Stream"
