# fugato.exceptions
# Custom exceptions for API
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Jan 21 14:59:27 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] bengfort@cs.umd.edu $

"""
Custom exceptions for API
"""

##########################################################################
## Imports
##########################################################################

from rest_framework.exceptions import APIException

##########################################################################
## API Exceptions
##########################################################################

class DuplicateQuestion(APIException):

    status_code = 400
    default_detail = "question has already been asked"
