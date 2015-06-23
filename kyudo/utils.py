# kyudo.utils
# Project level utilities
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Oct 23 14:09:04 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Project level utilities
"""

##########################################################################
## Imports
##########################################################################

import re
import base64
import bleach
import hashlib

from markdown import markdown

##########################################################################
## Utilities
##########################################################################

## Nullable kwargs for models
nullable = { 'blank': True, 'null': True, 'default':None }

## Not nullable kwargs for models
notnullable = { 'blank': False, 'null': False }

##########################################################################
## Helper functions
##########################################################################

def normalize(text):
    """
    Normalizes the text by removing all punctuation and spaces as well as
    making the string completely lowercase.
    """
    return re.sub(r'[^a-z0-9]+', '', text.lower())

def signature(text):
    """
    This helper method normalizes text and takes the SHA1 hash of it,
    returning the base64 encoded result. The normalization method includes
    the removal of punctuation and white space as well as making the case
    completely lowercase. These signatures will help us discover textual
    similarities between questions.
    """
    return base64.b64encode(hashlib.sha1(normalize(text)).digest())

def htmlize(text):
    """
    This helper method renders Markdown then uses Bleach to sanitize it as
    well as convert all links to actual links.
    """
    text = bleach.clean(text, strip=True)    # Clean the text by stripping bad HTML tags
    text = markdown(text)                    # Convert the markdown to HTML
    text = bleach.linkify(text)              # Add links from the text and add nofollow to existing links

    return text

