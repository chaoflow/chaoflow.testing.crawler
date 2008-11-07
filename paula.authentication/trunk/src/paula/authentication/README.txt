Currently unused


paula.authentication README.txt
===============================

This file serves as an integration test of paula.authentication with
a PluggableAuthenticationUtility.

Our configure.zcml registered our plugins globally, named "Paula Authenticator
Plugin" and "Paula Mapping Credentials Plugin". Let's check whether they are
there:

    >>> ap_name = 'Paula Authenticator Plugin'
    >>> cp_name = 'Paula Mapping Credentials Plugin'

    >>> from zope.app.authentication import interfaces
    >>> getUtility(interfaces.IAuthenticatorPlugin, ap_name) is not None
    True
    >>> getUtility(interfaces.ICredentialsPlugin, cp_name) is not None
    True


In order to use them, you need to have a PAU and tell it about them.


PAU factories, provided globally as multi-adapters from 
(IPrincipalInfo, IRequest) to the resp. factory interface.

    >>> from zope.app.authentication import principalfolder
    >>> provideAdapter(principalfolder.AuthenticatedPrincipalFactory)
    >>> provideAdapter(principalfolder.FoundPrincipalFactory)

create a PAU,

    >>> from zope.app.authentication import PluggableAuthentication
    >>> pau = PluggableAuthentication()
    
register plugins. Take care, PAU won't complain, but just won't authenticated,
if you misspell...

    >>> pau.authenticatorPlugins = (ap_name,)
    >>> pau.credentialsPlugins = (cp_name,)


In order to have authentication data, we use a mockup auth provider utility.
It is the job of paula.authutil to test its integration with us, here we do
not want to be dependent on its correct implementation.

Create mockup auth provider and auth provider utility

    >>> from paula.authentication.interfaces import IAuthProvider
    >>> from paula.authentication.interfaces import IAuthProviders

    >>> ap = Mock(id="global", validate = lambda login=None,password=None: \\
    ...         password == "correct")
    >>> alsoProvides(ap, IAuthProvider)

    >>> class MockAPU(object):
    ...     implements(IAuthProviders)
    ...     def __getitem__(self, id):
    ...         return ap

    >>> apu = MockAPU()
    >>> provideUtility(apu, IAuthProviders)


Try to authenticate

    >>> import UserDict
    >>> from zope.publisher.interfaces import IRequest
    >>> req = UserDict.UserDict()
    >>> alsoProvides(req, IRequest)

no credentials

    >>> print pau.authenticate(req)
    None

wrong credentials

    >>> req['login'] = "global"
    >>> req['password'] = "wrong"
    >>> print pau.authenticate(req)
    None

correct credentials

    >>> req['password'] = "correct"
    >>> pau.authenticate(req)
    Principal('global')


Now all components (PAU, our AuthenticatorPlugin and credentials plugin, and
the mock AuthProviders) were registered globally. Let's make sure that
everything works, when providing context.

Get the root folder and make sure it is a site

    >>> from zope.location.interfaces import ISite
    >>> root = getRootFolder()
    >>> ISite.providedBy(root)
    True

Check that our site's manager and the global site manager are different

    >>> gsm = getSiteManager()
    >>> sm = root.getSiteManager()
    >>> gsm is not sm
    True

make sure, that also zope.component's getSiteManager knows about this,
I managed to create situations, where it did not...

    >>> getSiteManager(context=root) is gsm
    False
    >>> getSiteManager(context=root) is sm
    True



create another pau, that is contained in our new site and let it now about the
same plugins, it should find them when being contained.

    >>> loc_pau = PluggableAuthentication()
    >>> loc_pau.authenticatorPlugins = (ap_name,)
    >>> loc_pau.credentialsPlugins = (cp_name,)
    >>> root['loc_pau'] = loc_pau

In the context of our local pau, we should get our site's site manager

    >>> getSiteManager(context=loc_pau) is sm
    True

However, we need to provide a different authenticator plugin, that is aware of
location, i.e. uses context for retrieving utilities.

    >>> from zope.app.authentication.interfaces import IAuthenticatorPlugin
    >>> from paula.authentication import LocalAuthenticatorPlugin
    >>> from paula.authentication.interfaces import ILocalAuthenticatorPlugin

    >>> loc_pau_ap = LocalAuthenticatorPlugin()
    >>> root['loc_pau_ap'] = loc_pau_ap

    >>> getSiteManager(context=loc_pau_ap) is sm
    True


as long as we do not register, it will not be in the context of our local pau

    >>> sm_pau_ap = getUtility(IAuthenticatorPlugin, context=loc_pau,
    ...         name=ap_name)
    >>> ILocalAuthenticatorPlugin.providedBy(sm_pau_ap)
    False

    >>> sm.registerUtility(loc_pau_ap, ILocalAuthenticatorPlugin, name=ap_name)
    >>> sm_pau_ap = getUtility(IAuthenticatorPlugin, context=loc_pau,
    ...         name=ap_name)
    >>> ILocalAuthenticatorPlugin.providedBy(sm_pau_ap)
    True


Authentication with the credentials in the global registry still works

    >>> loc_pau.authenticate(req)
    Principal('global')


Now, let's create a new auth provider utility, with a different auth provider

    >>> loc_ap = Mock(id="local", validate = lambda login=None,password=None: \
    ...         password == "local")
    >>> alsoProvides(loc_ap, IAuthProvider)

    >>> class MockAPU(object):
    ...     implements(IAuthProviders)
    ...     def __getitem__(self, id):
    ...         return loc_ap

    >>> loc_apu = MockAPU()

still the global utility

    >>> sm.getUtility(IAuthProviders) is apu
    True

now the local one

    >>> sm.registerUtility(loc_apu, IAuthProviders)
    >>> sm.getUtility(IAuthProviders) is loc_apu
    True

a request corresponding to the credentials in the local registry

    >>> loc_req = UserDict.UserDict()
    >>> alsoProvides(loc_req, IRequest)
    >>> loc_req['login'] = 'local'
    >>> loc_req['password'] = 'local'


Both levels, global and local, do not collide.

    >>> loc_pau.authenticate(loc_req)
    Principal('local')
    >>> loc_pau.authenticate(req) is None
    True

    >>> pau.authenticate(loc_req) is None
    True
    >>> pau.authenticate(req)
    Principal('global')
