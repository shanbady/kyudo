# kyudo.views
# Views for the project and application that don't require models
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 01 17:55:52 2014 -0400
#
# Copyright (C) 2014 University of Maryland
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the project and application that don't require models
"""

##########################################################################
## Imports
##########################################################################

from django.shortcuts import redirect
from users.mixins import LoginRequired, is_member
from django.views.generic import TemplateView

##########################################################################
## Application Views
##########################################################################

class SplashPage(TemplateView):
    """
    Main splash page for the app. Although this is essentially a simple
    webpage with no need for extra context, this view does check if the
    user is logged in, and if so, immediately redirects them to the app.
    """

    template_name = "site/index.html"

    def dispatch(self, request, *args, **kwargs):
        """
        If a user is authenticated, redirect to the Application, otherwise
        serve normal template view as expected.
        """
        if request.user.is_authenticated():
            return redirect('app-root', permanent=False)
        return super(SplashPage, self).dispatch(request, *args, **kwargs)

class WebAppView(LoginRequired, TemplateView):
    """
    Authenticated web application view that serves all context and content
    to kick off the Backbone front-end application.
    """

    template_name = "app/index.html"
