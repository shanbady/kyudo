# voting.apps
# Describes the Voting application for Django
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 23:34:16 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: apps.py [] bengfort@cs.umd.edu $

"""
Describes the Voting application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Voting Config
##########################################################################

class VotingConfig(AppConfig):
    name = 'voting'
    verbose_name = "Voting"

    def ready(self):
        import voting.signals
