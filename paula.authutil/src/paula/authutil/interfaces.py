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

from zope.interface import Interface

from paula.authentication.interfaces import IAuthProviders


class PrincipalIdAlreadyTaken(Exception):
    """Indicates that a principal with the same id is already registered
    """

class IAuthProviderAdaptable(Interface):
    """Marker interface for objects that can be adapted to IAuthProvider
    """

class IRWAuthProviders(IAuthProviders):
    """A IAuthProviders where objects can be registered/unregistered.
    """

    def register(obj):
        """Register an object

        It is assumed that the object provides IAuthProviderAdaptable and
        an adapter for IAuthProvider is available, an AdaptationError is
        raised otherwise.

        Fails with PrincipalIdAlreadyTaken, in case an object with the same
        principal id is registered already.
        """

    def unregister(obj):
        """Unregister an object.

        Fails with KeyError, if the object is not registered.
        """
