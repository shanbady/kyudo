# kyudo.version
# Helper module for managing versioning information
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Jun 23 11:49:35 2015 -0400
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: version.py [] benjamin@bengfort.com $

"""
Helper module for managing versioning information
"""

##########################################################################
## Versioning
##########################################################################

__version_info__ = {
    'major': 1,
    'minor': 0,
    'micro': 4,
    'releaselevel': 'final',
    'serial': 0,
}


def get_version(short=False):
    """
    Returns the version from the version info.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)
