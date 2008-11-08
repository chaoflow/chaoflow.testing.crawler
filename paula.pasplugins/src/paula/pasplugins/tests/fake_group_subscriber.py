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
from zope.security.interfaces import IGroupAwarePrincipal
from zope.component import adapter, queryUtility

from paula.pasplugins.tests.fake_pau_ap import FAKE_LOGIN

@adapter(IPrincipalCreated)
def setGroupsForPrincipal(event):
    """Put groups onto the principal
    """
    principal = event.principal
    if not IGroupAwarePrincipal.providedBy(principal):
        return None
   
    if principal.id == FAKE_LOGIN:
        principal.groups.extend(['fakegroup1', 'fakegroup2'])
