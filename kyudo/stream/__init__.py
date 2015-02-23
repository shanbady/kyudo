# stream
# An App that implements an Activity Stream for Kyudo
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Feb 04 10:21:07 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
An App that implements an Activity Stream for Kyudo.

Activity Streams (or newsfeeds) are user specific events on a system. They
are becoming more popular, and even have a W3C specification!

See http://www.w3.org/TR/2014/WD-activitystreams-core-20141023/
"""

##########################################################################
## Imports
##########################################################################

from signals import stream
