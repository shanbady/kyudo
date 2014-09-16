# kyudo.settings.base
# The common Django settings for Kyodo project
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Sep 12 16:09:51 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: base.py [] bengfort@cs.umd.edu $

"""
Django settings for kyudo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os
from django.conf import global_settings

##########################################################################
## Helper function for environmental settings
##########################################################################

def environ_setting(name, default=None):
    """
    Fetch setting from the environment- if not found, then this setting is
    ImproperlyConfigured.
    """
    if name not in os.environ and default is None:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            "The {0} ENVVAR is not set.".format(name)
        )

    return os.environ.get(name, default)

##########################################################################
## Build Paths inside of project with os.path.join
##########################################################################

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(BASE_DIR, os.pardir))

##########################################################################
## Secret settings - do not store!
##########################################################################

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ_setting("SECRET_KEY")

##########################################################################
## Database Settings
##########################################################################

## See https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ_setting('DB_NAME', 'kyudo'),
        'USER': environ_setting('DB_USER', 'django'),
        'PASSWORD': environ_setting('DB_PASS', ''),
        'HOST': environ_setting('DB_HOST', 'localhost'),
        'PORT': environ_setting('DB_PORT', '5432'),
    },
}

##########################################################################
## Runtime settings
##########################################################################

## Debugging settings
## SECURITY WARNING: don't run with debug turned on in production!
DEBUG          = True
TEMPLATE_DEBUG = True

## Hosts
ALLOWED_HOSTS  = []
INTERNAL_IPS   = ('127.0.0.1', '198.168.1.10')

## WSGI Configuration
ROOT_URLCONF     = 'kyudo.urls'
WSGI_APPLICATION = 'kyudo.wsgi.application'

## Application definition
INSTALLED_APPS = (
    # Django apps
    'grappelli', # Must come before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'social.apps.django_app.default',

    # Kyudo apps
    'users',
)

## Request Handling
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

## Internationalization
## https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True

## Admin Title
GRAPPELLI_ADMIN_TITLE = "Kyudo Admin"

##########################################################################
## Content (Static, Media, Templates)
##########################################################################

## Static files (CSS, JavaScript, Images)
## https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL          = '/static/'

STATICFILES_DIRS    = (
    os.path.join(PROJECT_DIR, 'static'),
)

## Template Files.
TEMPLATE_DIRS       = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

## Uploaded Media
MEDIA_URL           = "/media/"

##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'benjamin@bengfort.com'),
)

SERVER_EMAIL    = 'Dakota <server@bengfort.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER = 'server@bengfort.com'
EMAIL_HOST_PASSWORD  = environ_setting("EMAIL_HOST_PASSWORD")
EMAIL_PORT      = 587
EMAIL_SUBJECT_PREFIX = '[KYUDO]'

##########################################################################
## Authentication
##########################################################################

LOGIN_URL = '/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Google OAuth2 Credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = environ_setting("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_SECRET")
