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

from zope.app.authentication.authentication import PluggableAuthentication
from zope.interface import alsoProvides, implements

from paula.pau_addons.interfaces import IPaulaAuthentication
from paula.pau_addons.interfaces import IPropertyInterface


def copy_properties( src, dest):
    """
    A mockup destination

        >>> dest = Mock(id='1')

    A mockup source

        >>> class IA(Interface):
        ...     a1 = Attribute(u"a1")
        ...     a2 = Attribute(u"a2")
        >>> alsoProvides(IA, IPropertyInterface)

        >>> class IB(Interface):
        ...     b = Attribute(u"b")
        >>> alsoProvides(IB, IPropertyInterface)

        >>> class IC(Interface):
        ...     c = Attribute(u"c")

        >>> src = Mock(
        ...         a1=1,
        ...         a2=2,
        ...         b=3,
        ...         c='not copied',
        ...         alsoProvides=(IA,IB),
        ...         )

    Call and check which attributes made it

        >>> copy_properties(src, dest)
        >>> IA.providedBy(dest)
        True
        >>> IB.providedBy(dest)
        True
        >>> IC.providedBy(dest)
        False
        >>> dest.a1
        1
        >>> dest.a2
        2
        >>> dest.b
        3
        >>> getattr(dest, 'c', 'foo')
        'foo'
    """
    schemas = list(src.__provides__)
    for schema in schemas:
        # only use interfaces that defined properties
        if not IPropertyInterface.providedBy(schema):
            continue
        # iterate over schema fields and copy values
        # also see comment below, dynamic lookup would be great
        for name in list(schema):
            value = getattr(schema(src), name)
            setattr(dest, name, value)
        alsoProvides(dest, schema)

        #XXX: this is not working, as property object most probably
        #     do magic inside of __getattr__ and rely on classes to
        #     interpret them correctly.
        #     Another way would be to monkey-patch user's
        #     __getattr__...
        #     For now we leave it static, i.e. the values are taken
        #     only once and are not dynamically updated. Not sure,
        #     whether it is useful anyway, as I don't know how long
        #     Principals exist at all.
        #prop = property( lambda self: getattr(principal, name))
        #setattr(user, name, prop)


class PaulaAuthentication(PluggableAuthentication):
    """
    """
    implements(IPaulaAuthentication)

    def addUser(self, login, password):
        """
        """
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.addUser
            except AttributeError:
                continue

            if method(login, password):
                return True

        return False

    def delPrincipal(self, id):
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.delPrincipal
            except AttributeError:
                continue

            if method(login):
                return True

        return False


    def allowDeletePrincipal(self, id):
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.allowDeletePrincipal
            except AttributeError:
                continue

            if method(id):
                return True

        return False

    def allowPasswordSet(self, id):
        """
        """
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.allowPasswordSet
            except AttributeError:
                continue

            if method(id):
                return True

        return False

    def doChangeUser(self, login, password, **kws):
        """
        """
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.doChangeUser
            except AttributeError:
                continue

            if method(login, password, **kws):
                return True

        return False

    def setPropertiesForUser(self, login, **props):
        #XXX: this is bad and should not go via the auth plugin!!
        # it's also very specific to citymob
        auths = self.getAuthenticatorPlugins()
        for name, plugin in auths:
            try:
                method = plugin.setPropertiesForUser
            except AttributeError:
                continue

            if method(login, **props):
                return True

        raise RuntimeError
