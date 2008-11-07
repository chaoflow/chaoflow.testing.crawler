Currently unused



paula.examples Package Readme
=============================

XXX: zcml testing

    >>> from zope.component import provideAdapter
    >>> from zope.interface import providedBy

Create minimal plone user used for testing:

    >>> from paula.examples.content import MinimalPloneUser
    >>> user = MinimalPloneUser(
    ...         name='user',
    ...         password='pass',
    ...         email='foo@bar.com',
    ...         realname='Max Mustermann',
    ...         )


Test integration with auth utility:

Setup adapters

    >>> from paula.examples.adapters import AuthProviderFromBasicUser
    >>> provideAdapter(AuthProviderFromBasicUser)

Create paula auth utility

    >>> from paula.authutil import RWAuthProviders
    >>> apu = RWAuthProviders()

Register user with auth provider utility

    >>> apu.register(user)

Check whether user can be retrieved and used for validation

    >>> from paula.authentication.interfaces import IAuthProvider
    >>> authutil = IAuthProvider(apu['user'])
    >>> authutil.validate(login='user', password='pass')
    True


Test integration with property utility:

Setup adapters

    >>> from paula.examples.adapters import BasicPropertyProvider
    >>> provideAdapter(BasicPropertyProvider)

Create paula property utility

    >>> from paula.proputil import RWPropertyProviders
    >>> ppu = RWPropertyProviders()

Register user with property utility

    >>> ppu.register(user)

Check whether properties can be retrieved

    >>> from paula.properties.interfaces import IPropertyProvider
    >>> from paula.examples.interfaces import IMinimalPloneProperties
    >>> pps = ppu['user']
    >>> len(pps) == 1
    True
    >>> pp = pps[0]
    >>> IPropertyProvider.providedBy(pp)
    True
    >>> IMinimalPloneProperties.providedBy(pp)
    True
    >>> pp.id
    'user'
    >>> getattr(pp, 'password', 'foo')
    'foo'
    >>> pp.email
    'foo@bar.com'
    >>> pp.realname
    'Max Mustermann'
