from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    ## Authentication
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    ## Static pages
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    ## Admin site
    url(r'^admin/', include(admin.site.urls)),
)
