Currently unused


paula.properties Package Readme
===============================

XXX: eventually we just test this inside of paula.suite or wherever we do
the overall testing, it is way to bothersome to do it here...

Create two PAU's

    >>> from zope.app.authentication



test whether properties end up on principals created by a PAU


nested

two principals with the same name

two provider on one level for the same principal

another provider for another principal




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

    A mockup property provider utility

        >>> import UserDict
        >>> ppu = UserDict.UserDict()
        >>> ppu["1"] = [pp1, pp2]

    Call and check which attributes made it

        >>> _copy_attributes_from_ppu(p, ppu)
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
