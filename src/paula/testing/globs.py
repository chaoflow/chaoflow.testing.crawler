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

from UserDict import UserDict
from UserList import UserList

from zope.component import provideAdapter, provideUtility
from zope.component import adapts
from zope.component import getUtility, queryUtility
from zope.component import getSiteManager

from zope.interface import alsoProvides, implements, providedBy
from zope.interface import Interface, Attribute

from paula.testing import interact
from paula.testing import mock

test_globs = dict(
        Attribute = Attribute,
        Interface = Interface,
        Mock = mock.Mock,
        UserDict = UserDict,
        UserList = UserList,
        adapts = adapts,
        alsoProvides = alsoProvides,
        getUtility = getUtility,
        getSiteManager = getSiteManager,
        interact = interact.interact,
        implements = implements,
        provideAdapter = provideAdapter,
        provideUtility = provideUtility,
        providedBy = providedBy,
        queryUtility = queryUtility,
        )
