from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from users.views import ProfileView

urlpatterns = patterns('',
    ## Authentication
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    ## Static pages
    url(r'^$', TemplateView.as_view(template_name='site/index.html'), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    ## Admin site
    url(r'^admin/', include(admin.site.urls)),
)
