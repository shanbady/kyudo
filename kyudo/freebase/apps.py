# freebase.apps
# Describes the Freebase application for Django
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 16:04:14 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: apps.py [] bengfort@cs.umd.edu $

"""
Describes the Freebase application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Freebase Config
##########################################################################

class FreebaseConfig(AppConfig):
    name = 'freebase'
    verbose_name = "Freebase"

    def ready(self):
        import freebase.signals
