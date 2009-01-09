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

import types

from zope.interface import alsoProvides, implements, Interface

class Mock(object):
    """a mock object that carries desired interfaces

        >>> class IA(Interface):
        ...     pass
        >>> class IB(Interface):
        ...     pass
        >>> class IC(Interface):
        ...     pass

        >>> m = Mock( a = 1, f = lambda : 2, alsoProvides=(IA,IB))
        >>> m.a
        1
        >>> m.f()
        2
        >>> IA.providedBy(m)
        True
        >>> IB.providedBy(m)
        True
        >>> m = Mock( a = 1, f = lambda : 2, alsoProvides=IC)
        >>> IC.providedBy(m)
        True
    """
    implements(Interface)

    def __init__(self, **kws):
        try:
            alsoprovides = kws['alsoProvides']
        except KeyError:
            pass
        else:
            if type(alsoprovides) is types.TupleType:
                alsoProvides(self, *alsoprovides)
            else:
                alsoProvides(self, alsoprovides)
            del kws['alsoProvides']

        for k,v in kws.items():
            setattr(self, k, v)
