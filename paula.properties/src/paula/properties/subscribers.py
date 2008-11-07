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

from zope.component import adapter, queryUtility
from zope.interface import alsoProvides

from paula.properties.interfaces import IPropertyInterface
from paula.properties.interfaces import IPropertyProvider
from paula.properties.interfaces import IPropertyProviders

def _copy_attributes_from_ppu( principal, pps):
    """
    A mockup principal

        >>> p = Mock(id='1')

    A mockup property provider

        >>> class IA(Interface):
        ...     a1 = Attribute(u"a1")
        ...     a2 = Attribute(u"a2")
        >>> alsoProvides(IA, IPropertyInterface)

        >>> class IB(Interface):
        ...     b = Attribute(u"b")
        >>> alsoProvides(IB, IPropertyInterface)

        >>> class IC(Interface):
        ...     c = Attribute(u"c")

        >>> pp1 = Mock(
        ...         a1=1,
        ...         a2=2,
        ...         b=3,
        ...         c='not copied',
        ...         alsoProvides=(IA,IB),
        ...         )

    And another one

        >>> class ID(Interface):
        ...     d = Attribute(u"d")
        >>> alsoProvides(ID, IPropertyInterface)

        >>> pp2 = Mock(d=4, alsoProvides=(ID,))

    A list of property provider utilities

        >>> pps = [pp1, pp2]

    Call and check which attributes made it

        >>> _copy_attributes_from_ppu(p, pps)
        >>> IA.providedBy(p)
        True
        >>> IB.providedBy(p)
        True
        >>> IC.providedBy(p)
        False
        >>> ID.providedBy(p)
        True
        >>> p.a1
        1
        >>> p.a2
        2
        >>> p.b
        3
        >>> getattr(p, 'c', 'foo')
        'foo'
        >>> p.d
        4
    """
    for pp in pps:
        schemas = list(pp.__provides__)
        for schema in schemas:
            # only use interfaces that defined properties
            if not IPropertyInterface.providedBy(schema):
                continue
            # iterate over schema fields and copy values
            # also see comment below, dynamic lookup would be great
            for name in list(schema):
                value = getattr(schema(pp), name)
                setattr(principal, name, value)
            alsoProvides(principal, schema)


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


@adapter(IPrincipalCreated)
def setPropertiesForPrincipal(event):
    """Put properties onto the principal

    The properties are directly stored as attributes. Magic happens in
    _copy_attributes_from_ppu, here we just get the utility and are tested
    in README.txt
    """
    principal = event.principal
    # we search for a property provider utility in the context of the auth
    # plugin that authenticated the principal, if there is none, we do
    # nothing
    ppu = queryUtility(
            IPropertyProviders,
    #        context=getSite(),
            )
    # XXX: for some reason a ppu is False
    if ppu is not None and principal.id in ppu:
        pps = ppu[principal.id]
        _copy_attributes_from_ppu( principal, pps)
