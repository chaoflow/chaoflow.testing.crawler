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

from zope.component import adapts
from zope.interface import alsoProvides, implements, Interface
from zope.interface import providedBy

from paula.authentication.interfaces import IAuthProvider

from paula.grouputil.interfaces import IMembershipProvider

from paula.properties.interfaces import IPropertyProvider
from paula.properties.interfaces import IPropertyInterface

from paula.examples.interfaces import IBasicUser
from paula.examples.interfaces import IBasicGroup


class AuthProviderFromBasicUser(object):
    """Basically a read-only wrapper demonstrating the concept

        >>> content = Mock(title='user', password='correct')
        >>> adapter = AuthProviderFromBasicUser(content)
        >>> adapter.id == content.title
        True
        >>> adapter.validate(login='foo', password='correct')
        True
        >>> adapter.validate(login='foo', password='wrong')
        False
    """
    adapts(IBasicUser)
    implements(IAuthProvider)

    @property
    def id(self):
        return self.context.title
    
    def __init__(self, context):
        self.context = context

    def validate(self, login=u"", password=u""):
        return password == self.context.password


class BasicPropertyProvider(object):
    """This provides the same IPropertyInterface-providing interfaces as the
    adpated context provides, and all attributes not defined on self,
    are passed on to the context.

        >>> from zope.interface import alsoProvides, Attribute
        >>> content = Mock(
        ...         title='login',
        ...         password='pass',
        ...         email='foo@bar',
        ...         )

        >>> class IA(Interface):
        ...     email = Attribute('email')

        >>> alsoProvides(content, IA)
        >>> alsoProvides(IA, IPropertyInterface)
        
        >>> adapter = BasicPropertyProvider(content)
        >>> adapter.id == content.title
        True
        >>> adapter.email == content.email
        True
        >>> getattr(adapter, 'password', 'foo')
        'foo'
        >>> IPropertyProvider.providedBy(adapter)
        True
        >>> IA.providedBy(adapter)
        True
    """
    adapts(Interface)
    implements(IPropertyProvider)

    @property
    def id(self):
        return self.context.title

    def __init__(self, context):
        """
        """
        propifs = filter(
                IPropertyInterface.providedBy,
                list(providedBy(context)),
                )
        alsoProvides(self, propifs)
        self.context = context

    def __getattr__(self, name):
        props = []
        for x in list(providedBy(self)):
            props += list(x)
        if name not in props:
            raise AttributeError
        return getattr(self.context, name)


class MembershipProviderFromBasicGroup(object):
    """
    """
    adapts(IBasicGroup)
    implements(IMembershipProvider)

    def __init__(self, context):
        self.context = context

    @property
    def groups(self):
        return (self.context.title,)

    @property
    def members(self):
        return tuple(self.context.members)
