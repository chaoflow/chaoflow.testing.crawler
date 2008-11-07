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
from zope.schema import List

from paula.groups.interfaces import IMemberships


class IMembershipProvider(Interface):
    """A membership provider associates 1..n principals with 1..m groups

    In order to get all members of a group and all groups of a principal,
    the information of several providers is combined.

    The most common providers will associate one group with several members
    (classic group) or one member with several groups (groups stored on the
    prinicipal).
    """
    groups = List(
            title=u"Groups",
            description=u"The groups this provider defines members for",
            )

    members = List(
            title=u"Members",
            description=u"The members of the groups",
            )


class IMembershipProviderAdaptable(Interface):
    """Marker interface for objects that can be adapted to IMembershipProvider
    """


class IRWMemberships(IMemberships):
    """
    """

    def register(obj):
        """Register an object
        """

    def unregister(obj):
        """Unregister an object.
        """
