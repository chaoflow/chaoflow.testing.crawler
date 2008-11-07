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

from paula.properties.interfaces import IPropertyProviders


class IPropertyProviderAdaptable(Interface):
    """Marker interface for objects that can be adapted to IPropertyProvider
    """

class IRWPropertyProviders(IPropertyProviders):
    """A utility that returns property providers for principals
    """

    def register(obj):
        """Register an object

        It is assumed that the object provides IPropertyProviderAdaptable and
        an adapter for IPropertyProvider is available, a TypeError is raised
        otherwise.
        """

    def unregister(obj):
        """Unregister an object.

        Fails with ValueError, if the object is not registered.
        """

class ILocalRWPropertyProviders(IRWPropertyProviders):
    """
    """
