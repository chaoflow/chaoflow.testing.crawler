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

from plone.app.content.interfaces import INameFromTitle
from plone.app.content.container import Container

from plone.locking.interfaces import ITTWLockable

from zope.component.factory import Factory
from zope.interface import implements

from paula.examples.content import MinimalPloneUser as MinimalPloneUserBase
from paula.examples.content import BasicGroup as BasicGroupBase


class MinimalPloneUser(Container, MinimalPloneUserBase):
    """User content with minimal properties for plone

    realized as a container content type
    """
    implements(ITTWLockable, INameFromTitle)
    meta_type = portal_type = "Paula Minimal Plone User"

    def __init__(self, id=None, **kws):
        Container.__init__(self, id)
        MinimalPloneUserBase.__init__(self, **kws)

minimalPloneUserFactory = Factory(
        MinimalPloneUser,
        title=u"Create a minimal plone user",
        description=u"This factory instantiates new minimal plone users",
        )


class BasicGroup(Container, BasicGroupBase):
    """Basic Group content

    realized as a container content type
    """
    implements(ITTWLockable, INameFromTitle)
    meta_type = portal_type = "Paula Basic Group"

    def __init__(self, id=None, **kws):
        Container.__init__(self, id)
        BasicGroupBase.__init__(self, **kws)

basicGroupFactory = Factory(
        BasicGroup,
        title=u"Create a basic group",
        description=u"This factory instantiates new basic groups",
        )
