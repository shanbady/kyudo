# kyudo
# The kyudo project definition app
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 01 17:55:52 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
The kyudo project definition app
"""

##########################################################################
## Imports
##########################################################################

##########################################################################
## Module variables
##########################################################################

__version__ = (1, 0, 3)

##########################################################################
## Module functions
##########################################################################

def get_version():
    """
    Returns a string representation of the version.
    """
    return ".".join(["%i" % num for num in __version__])
