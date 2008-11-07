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

from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent

from zope.component import adapter, queryUtility

from zope.location.interfaces import ILocation

from paula.grouputil.interfaces import IMembershipProvider
from paula.grouputil.interfaces import IMembershipProviderAdaptable
from paula.grouputil.interfaces import IRWMemberships


@adapter(ILocation, IObjectAddedEvent)
def checkRegister(obj, event):
    """A subscriber to ObjectAddedEvent
    """
    if not IMembershipProviderAdaptable.providedBy(obj) and \
            not IMembershipProvider.providedBy(obj):
        return

    # we are registered globally and might run in a context without
    # IRWMemberships
    util = queryUtility(IRWMemberships) #, context=event.newParent)
    # XXX: not working, util is False?!
    #if util:
    if util is not None:
        util.register(obj)


@adapter(ILocation, IObjectRemovedEvent)
def checkUnregister(obj, event):
    """A subscriber to ObjectRemovedEvent
    """
    if not IMembershipProviderAdaptable.providedBy(obj) and \
            not IMembershipProvider.providedBy(obj):
        return

    # we are registered globally and might run in a context without
    # IRWMemberships
    util = queryUtility(IRWMemberships) #, context=event.newParent)
    # XXX: not working, util is False?!
    #if util:
    if util is not None:
        try:
            util.unregister(obj)
        except KeyError:
            pass
