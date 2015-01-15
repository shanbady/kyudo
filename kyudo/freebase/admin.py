# freebase.admin
# Admin site registration for Freebase models
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Jan 15 11:26:03 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Admin site registration for Freebase models
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from freebase.models import Topic, TopicAnnotation

# Register your models here.
admin.site.register(Topic)
admin.site.register(TopicAnnotation)
