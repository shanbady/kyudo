# fugato.apps
# Describes the Fugato application for Django
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 15:38:51 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: apps.py [] bengfort@cs.umd.edu $

"""
Describes the Fugato application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Fugato Config
##########################################################################

class FugatoConfig(AppConfig):
    name = 'fugato'
    verbose_name = "Fugato"

    def ready(self):
        import fugato.signals
