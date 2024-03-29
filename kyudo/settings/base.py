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
Django settings for houston project.

This file was adapated by the settings.py file generated by
'django-admin startproject' using Django 1.7 to be modified for Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

##########################################################################
## Imports
##########################################################################

import os

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

## Project is the location of the houston directory (with the wsgi.py)
## Repository is the location of the project and the apps and other files

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY = os.path.dirname(PROJECT)

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

## Hosts - specify in production settings
ALLOWED_HOSTS  = ["*"]
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
    'django.contrib.humanize',

    # Third party apps
    'social.apps.django_app.default',
    'rest_framework',

    # Kyudo apps
    'stream',   # Implements an activity stream for the app
    'users',    # Handles Google OAuth and Profiles
    'fugato',   # Initial query collection app
    'freebase', # Handles the knowledge base and RDF api
    'voting',   # Handles the upvoting and downvoting of objects
    'reasoner', # Simple case based reasoning prototype
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
    'django.middleware.security.SecurityMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

## Internationalization
## https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'America/New_York'
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
STATIC_URL          = '/assets/'

## Uploaded Media
MEDIA_URL           = "/media/"

STATICFILES_DIRS    = (
    os.path.join(PROJECT, 'assets'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

## Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]



##########################################################################
## Logging and Error Reporting
##########################################################################

ADMINS          = (
    ('Benjamin Bengfort', 'benjamin@bengfort.com'),
)

SERVER_EMAIL    = 'Kyudo Admin <server@bengfort.com>'
EMAIL_USE_TLS   = True
EMAIL_HOST      = 'smtp.gmail.com'
EMAIL_HOST_USER = environ_setting('EMAIL_HOST_USER', 'server@bengfort.com')
EMAIL_HOST_PASSWORD  = environ_setting('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT      = 587
EMAIL_SUBJECT_PREFIX = '[KYUDO] '

##########################################################################
## Authentication
##########################################################################

LOGIN_URL = '/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/app'

## Support for Social Auth authentication backends
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

## Google OAuth2 Credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    = environ_setting("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ_setting("GOOGLE_OAUTH2_SECRET")

## Freebase API Keys
FREEBASE_API_KEY                 = environ_setting("FREEBASE_API_KEY")

##########################################################################
## Django REST Framework
##########################################################################

REST_FRAMEWORK = {

    ## API Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    ## Default permissions to access the API
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    ## Pagination in the API
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGINATE_BY': 50,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 200,
}

##########################################################################
## Stanford Paths
##########################################################################

## NER JAR and Models
STANFORD_NER_MODEL = None
STANFORD_NER_JAR   = None

## Parser JAR and Models
STANFORD_PARSER_MODELS = None
STANFORD_PARSER_JAR    = None

## Parse on Save (change this to False if it's taking too long)
STANFORD_PARSE_ON_SAVE = True
