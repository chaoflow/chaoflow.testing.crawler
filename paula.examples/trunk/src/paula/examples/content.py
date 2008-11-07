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

from persistent import Persistent

from zope.app.container.contained import Contained
from zope.component.factory import Factory
from zope.interface import implements

from paula.examples.interfaces import IBasicUser
from paula.examples.interfaces import IMinimalPloneUser
from paula.examples.interfaces import IMinimalPloneProperties

from paula.examples.interfaces import IBasicGroup

from paula.authutil.interfaces import IAuthProviderAdaptable
from paula.proputil.interfaces import IPropertyProviderAdaptable
from paula.grouputil.interfaces import IMembershipProviderAdaptable


class BasicUser(Persistent, Contained):
    """A very basic user

        >>> title = u'name'
        >>> password = u'password'
        
        >>> b = BasicUser(
        ...         title=title,
        ...         password=password,
        ...         )
        >>> b.title == title
        True
        >>> b.password == password
        True
    """
    implements(
            IBasicUser,
            IAuthProviderAdaptable,
            )

    title = u""
    password = u""

    def __init__(self, title=None, password=None):
        self.title = title
        self.password = password


class MinimalPloneUser(BasicUser):
    """User content with minimal properties for plone

        >>> title = u'name'
        >>> password = u'password'
        >>> realname = u'realname'
        >>> email = u'email'
        
        >>> b = MinimalPloneUser(
        ...         title=title,
        ...         password=password,
        ...         realname=realname,
        ...         email=email,
        ...         )
        >>> b.realname == realname
        True
        >>> b.email == email
        True
    """
    # it is important to explicitly provide IMinimalPloneProperties
    # at least for our BasicPropertyProvider adapter
    implements(
            IMinimalPloneUser,
            IMinimalPloneProperties,
            IPropertyProviderAdaptable,
            )

    realname = u""
    email = u""

    def __init__(self,
            title=None,
            password=None,
            realname=None,
            email=None,
            ):
        BasicUser.__init__(
                self,
                title=title,
                password=password,
                )
        self.realname = realname
        self.email = email

minimalPloneUserFactory = Factory(
        MinimalPloneUser,
        title=u"Create a minimal plone user",
        description=u"This factory instantiates new minimal plone users",
        )


class BasicGroup(Persistent, Contained):
    """
    """
    implements(
            IBasicGroup,
            IMembershipProviderAdaptable,
            )

    title = u""
    members = []


basicGroupFactory = Factory(
        BasicGroup,
        title=u"Create a basic group",
        description=u"This factory instantiates new basic groups",
        )


