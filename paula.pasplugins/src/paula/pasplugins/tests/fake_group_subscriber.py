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

from zope.app.authentication.interfaces import IPrincipalCreated
from zope.app.component.hooks import getSite

from zope.security.interfaces import IGroupAwarePrincipal
from zope.component import adapter, queryUtility

from paula.groups.interfaces import IMemberships


@adapter(IPrincipalCreated)
def setGroupsForPrincipal(event):
    """Put groups onto the principal
    """
    principal = event.principal
    if not IGroupAwarePrincipal.providedBy(principal):
        return None

    # we search for a group membership utility in the context of the auth
    # plugin that authenticated the principal, if there is none, we do
    # nothing
    mu = queryUtility(
            IMemberships,
    #        context=getSite(),
            )
    # XXX: for some reason a mu is False
    if mu is None:
        return
    
    groups = mu.getGroupsForPrincipal(principal.id)
    principal.groups.extend(groups)
