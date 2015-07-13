# reasoner.views
# Views for the reasoning prototype app
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Jul 12 09:49:23 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the reasoning prototype app.
"""

##########################################################################
## Imports
##########################################################################

from users.mixins import LoginRequired
from django.views.generic import TemplateView

##########################################################################
## HTTP Generated Views
##########################################################################

class ReasonerPrototypeView(LoginRequired, TemplateView):

    template_name = "app/reasoner.html"
