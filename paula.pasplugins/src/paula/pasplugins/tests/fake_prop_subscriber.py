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
from zope.component import adapter
from zope.interface import alsoProvides, Interface, Attribute

from paula.pau_addons.interfaces import IPropertyInterface
from paula.pasplugins.tests.fake_pau_ap import FAKE_LOGIN

class IA(Interface):
    email = Attribute(u'email')
    realname = Attribute(u'realname')

class IB(Interface):
    foo = Attribute(u'foo')

alsoProvides(IA, IPropertyInterface)
alsoProvides(IB, IPropertyInterface)

@adapter(IPrincipalCreated)
def setPropertiesForPrincipal(event):
    """Put properties onto the principal

    The properties are directly stored as attributes.
    """
    principal = event.principal

    if principal.id == FAKE_LOGIN:
        principal.email = u'foo@bar.com'
        principal.realname = u'fake user'
        principal.foo = u'foo value'
        alsoProvides(principal, IA)
        alsoProvides(principal, IB)
