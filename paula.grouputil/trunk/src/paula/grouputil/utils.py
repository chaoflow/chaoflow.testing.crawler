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

from BTrees import OOBTree
from persistent import Persistent
from persistent.list import PersistentList

from zope.app.container.contained import Contained

from zope.component import adapter, queryUtility
from zope.component.interfaces import IFactory

from zope.interface import implements

from paula.grouputil.interfaces import IMembershipProvider

from paula.grouputil.interfaces import IMembershipProviderAdaptable
from paula.grouputil.interfaces import IRWMemberships


class RWMemberships(Persistent, Contained):
    """

        >>> mp1 = Mock(
        ...     groups=('g1',),
        ...     members=('p1','p2'),
        ...     alsoProvides=(IMembershipProvider,),
        ...     )
        >>> mp2 = Mock(
        ...     groups=('g1','g2'),
        ...     members=('p1', 'p3','p4'),
        ...     alsoProvides=(IMembershipProvider,),
        ...     )
        >>> mp3 = Mock(
        ...     groups=('g2','g3'),
        ...     members=('p1','p5'),
        ...     alsoProvides=(IMembershipProvider,),
        ...     )

        >>> mu = RWMemberships()
        >>> interact( locals() )
    """
    implements(IRWMemberships)

    def __init__(self):
        """
        """
        self._objs = PersistentList()
        self._members = queryUtility(IFactory, 'OOBTree', OOBTree.OOBTree)()
        self._groups = queryUtility(IFactory, 'OOBTree', OOBTree.OOBTree)()

    def getGroupsForPrincipal(self, id):
        """
        """
        try:
            return tuple(set(self._groups[id]))
        except KeyError:
            return ()

    def getMembersForGroup(self, id):
        """
        """
        try:
            return tuple(set(self._members[id]))
        except KeyError:
            return ()

    def register(self, obj):
        """Register an object.

        It is assumed that an adapter lookup for IMembershipProvider
        succeeds.
        """
        mp = IMembershipProvider(obj)
        for id in mp.members:
            try:
                groups = self._groups[id]
            except KeyError:
                self._groups[id] = PersistentList()
                groups = self._groups[id]
            groups.extend(mp.groups)

        for id in mp.groups:
            try:
                members = self._members[id]
            except KeyError:
                self._members[id] = PersistentList()
                members = self._members[id]
            members.extend(mp.members)

        self._objs.append(obj)

    def unregister(self, obj):
        """Unregister an object.

        Fails with ValueError, if the object is not registered.
        """
        mp = IMembershipProvider(obj)
        self._objs[id].remove(obj)
        for id in mp.members:
            for x in mp.groups:
                self._groups[id].remove(x)

        for id in mp.groups:
            for x in mp.members:
                self._members[id].remove(x)
