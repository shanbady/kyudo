#!/usr/bin/env python
# manage.py
# Django default management commands, with some special sauce.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jun 23 09:29:36 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: manage.py [] bengfort@cs.umd.edu $

"""
Django default management commands, with some special sauce.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import dotenv

##########################################################################
## Main Method
##########################################################################

if __name__ == "__main__":
    ## Manage Django Environment
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kyudo.settings.production")

    ## Execute Django utility
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
