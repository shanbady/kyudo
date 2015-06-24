# kyudo.urls
# The main URL router for the app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Sep 16 16:47:22 2014 -0400
#
# Copyright (C) 2014 University of Maryland
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
The main URL router for the app
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from django.views.generic import TemplateView

from kyudo.views import *
from users.views import *
from fugato.views import *
from freebase.views import *

##########################################################################
## Endpoint Discovery
##########################################################################

## API
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'freebase', FreebaseViewSet, "freebase")
router.register(r'parse', ParserViewSet, "parse")
router.register(r'status', HeartbeatViewSet, "status")
router.register(r'annotations', TopicAnnotationViewSet, "annotation")

##########################################################################
## URL Patterns for the app
##########################################################################

urlpatterns = patterns('',
    ## Admin site
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    ## Static pages
    url(r'^$', SplashPage.as_view(), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    ## Application Pages
    url(r'^debug/$', DebugView.as_view(), name='app-debug'),
    url(r'^app/$', WebAppView.as_view(), name='app-root'),
    url(r'^q/(?P<slug>[\w-]+)/$', QuestionDetail.as_view(), name='question'),
    url(r'^similarity/$', SimilarityView.as_view(), name='app-similarity'),

    ## Authentication
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    ## REST API Urls
    url(r'^api/', include(router.urls, namespace="api")),
)
