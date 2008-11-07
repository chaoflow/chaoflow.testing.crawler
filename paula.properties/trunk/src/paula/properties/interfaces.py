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
from zope.interface.interfaces import IInterface
from zope.schema import TextLine


class IPropertyInterface(IInterface):
    """Interfaces providing this interface are recognizes as interfaces defining
    properties.
    """

class IPropertyProvider(Interface):
    """A property provider provides certain interfaces that provide
    IPropertyInterface, and makes property values available through attribute
    access. Other interfaces that might be provided also are ignored.

    For each attribute a value needs to be retrievable (at least None),
    otherwise an AttributeError will be raised.

    The principal will carry copies of the properties as attributes and provide
    the same IPropertyInterface-providing interfaces.
    """
    id = TextLine(
            title=u"Id",
            description=u"The principal id this provider works for",
            )

class IPropertyProviders(Interface):
    """A utility that returns property providers for principals
    """
    def __getitem__(id):
        """returns list of IPropertyProvider for principal id
        """
