# Copyright (c) 2008 by Florian Friesdorf
#
# GNU Affero General Public License (AGPL)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
"""
"""
__author__ = "Florian Friesdorf <flo@chaoflow.net>"
__docformat__ = "plaintext"

from zope.app.authentication.interfaces import ICredentialsPlugin
from zope.interface import implements, alsoProvides
from zope.publisher.interfaces import IRequest

CREDPLUG_NAME = "Paula: PAU CredentialsFromMappingPlugin"


class CredentialsFromMappingPlugin(object):
    """Just returns a mapping it is passed

    Useful, if you use paula and PAU just for authentication but not for
    challenging, i.e./e.g. from PlonePAS you already get the credentials in a
    mapping and don't need to bother with challenging.

    May be registered globally, as only functionality is implemented.

        >>> cp = CredentialsFromMappingPlugin()
        >>> m = UserDict()
        >>> c = cp.extractCredentials(m)
        >>> c is m
        True
        >>> IRequest.providedBy(m)
        True
    """
    implements(ICredentialsPlugin)
    
    def extractCredentials(self, mapping):
        """
        """
        # tune the mapping, PAU needs an IRequest to find its factories
        # If this does not work, better let the AttributeError go here, than
        # later in the getMultiAdapter lookup of PAU
        if not IRequest.providedBy(mapping):
            alsoProvides(mapping, IRequest)

        return mapping
    
    def challenge(self, request):
        pass # challenge is a no-op for this plugin
    
    def logout(self, request):
        pass # logout is a no-op for this plugin

