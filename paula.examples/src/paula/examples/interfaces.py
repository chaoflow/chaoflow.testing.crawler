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

from zope.interface import Interface, alsoProvides
from zope.schema import List, Object, TextLine, Password

from paula.properties.interfaces import IPropertyInterface


class IBasicUser(Interface):
    """Basic user

    Everything needed to do authentication, nothing more or less.
    """
    title = TextLine(
            title=u"Name",
            description=u"The user's login name (unique within an"
                    "authentication realm).",
            required=True,
            )

    password = Password(
            title=u"Password",
            description=u"The user password.",
            required=True,
            )


class IMinimalPloneProperties(Interface):
    """Minimal properties for plone
    """
    realname = TextLine(
            title=u"Realname",
            description=u"The user's realname.",
            required=True,
            )

    email = TextLine(
            title=u"Email",
            description=u"Email for user contact and password reset.",
            required=True,
            )

alsoProvides(IMinimalPloneProperties, IPropertyInterface)


class IMinimalPloneUser(IBasicUser,IMinimalPloneProperties):
    """A user with minimal properties needed for plone
    """


class IBasicGroup(Interface):
    """Basic group content type

    Everything needed to store information about group members in one place.
    This is a good thing to inherit from, for more sophisticated content types.
    """

    title = TextLine(
            title=u"Name",
            description=u"The group name (unique within an authentication realm).",
            required=True,
            )

    members = List(
            title=u"Members",
            description=u"List of member principal ids.",
            )
