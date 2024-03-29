# users.apps
# Describes the Users application for Django
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Mar 04 23:29:51 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: apps.py [] bengfort@cs.umd.edu $

"""
Describes the Users application for Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Freebase Config
##########################################################################

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "User Profiles"

    def ready(self):
        import users.signals
