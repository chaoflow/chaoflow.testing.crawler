Currently unused


paula.authutil Package Readme
=============================

This file serves as an integration test of paula.authutil with
paula.authentication.

Our configure.zcml registered a global RWAuthProviders. Let's check,
whether it is there

    >>> from paula.authutil.interfaces import IRWAuthProviders
    >>> global_apu = getUtility(IRWAuthProviders)
    >>> global_apu is not None
    True

Further, we included paula.authentication, so there should be a global
AuthenticatorPlugin available

    >>> from paula.authentication.interfaces import IAuthenticatorPlugin
    >>> global_ap = getUtility(
    ...         IAuthenticatorPlugin,
    ...         'Paula Authenticator Plugin',
    ...         )
    >>> global_ap is not None
    True

Let's create a subsite

    >>> from zope.app.component import site
    >>> from zope.app.folder import Folder
    >>> class SubSiteFolder(Folder, site.SiteManagerContainer):
    ...     pass
    >>> subsite = SubSiteFolder()
    >>> subsm = site.LocalSiteManager(subsite)
    >>> subsite.setSiteManager(subsm)

    >>> root = getRootFolder()
    >>> root['subsite'] = subsite

and add authenticator plugin and auth provider utility

    >>> from paula.authentication import LocalAuthenticatorPlugin
    >>> local_ap = LocalAuthenticatorPlugin()
    >>> root['subsite']['local_ap'] = local_ap

    >>> from paula.authutil import LocalRWAuthProviders
    >>> local_apu = LocalRWAuthProviders()
    >>> root['subsite']['local_apu'] = local_apu
    >>> subsm.registerUtility(local_apu, IRWAuthProviders)


auth provider content added directly to the root folder, should only end up
in the global auth provider utility and not the subsite one, and content
added to the subsite should only end up there and not in the global.

The subscribers should be fine with objects that directly implement
IAuthProvider, further down, we will check, whether they also work with
IAuthProviderAdaptable.

an incomplete mockup auth provider is added nowhere

    >>> ap1 = Mock(id="global", validate = lambda login=None,password=None: \
    ...         passord is "correct")
    >>> root['ap1'] = ap1
    >>> len(global_apu)
    0
    >>> len(local_apu)
    0
    >>> del root['ap1']

Let it provide IAuthProvider...

    >>> from paula.authentication.interfaces import IAuthProvider
    >>> alsoProvides(ap1, IAuthProvider)
    >>> root['ap1'] = ap1
    >>> len(global_apu)
    1
    >>> len(local_apu)
    0

Try to authenticate

    >>> g_creds = dict(login = "global", password = "correct")
    >>> global_ap.authenticateCredentials(g_creds)
    PrincipalInfo('global')
    >>> local_ap.authenticateCredentials(g_creds) is None
    True

Let's add another one within the subsite

    >>> ap2 = Mock(id="global", validate = lambda login=None,password=None: \
    ...         passord is "correct")
    >>> root['subsite']['ap2'] = ap2
    >>> len(global_apu)
    1
    >>> len(local_apu)
    0
    >>> del root['subsite']['ap2']

    >>> alsoProvides(ap2, IAuthProvider)
    >>> root['subsite']['ap2'] = ap2
    >>> len(global_apu)
    1
    >>> len(local_apu)
    1

The global is still only in the global

    >>> global_ap.authenticateCredentials(g_creds)
    PrincipalInfo('global')
    >>> local_ap.authenticateCredentials(g_creds) is None
    True

and the local is only in the local

    >>> loc_creds = dict(login = "local", password = "correct")
    >>> global_ap.authenticateCredentials(loc_creds) is None
    True
    >>> local_ap.authenticateCredentials(loc_creds)
    PrincipalInfo('local')


Removing them from the hierarchy needs to remove them from the utilities.

    >>> del root['ap1']
    >>> len(global_apu)
    0
    >>> len(local_apu)
    1
    >>> del root['subsite']['ap2']
    >>> len(global_apu)
    0
    >>> len(local_apu)
    0

The same should happen for IAuthProviderAdaptable, if there is an adapter
available.

    >>> from paula.authutil.interfaces import IAuthProviderAdaptable
    
    >>> class MockAdapter(object):
    ...     adapts(IAuthProviderAdaptable)
    ...     implements(IAuthProvider)
    ...     def __init__(self, context):
    ...         self.context = context
    ...     def __getattr__(self, attr):
    ...         getattr(self.context, attr)

    >>> ap3 = Mock(id="global", validate = lambda login=None,password=None: \
    ...         passord is "correct")
    >>> alsoProvides(ap3, IAuthProviderAdaptable)
    
    >>> root['ap3'] = ap3 #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        foo
    TypeError: foo
    >>> del root['ap3']

    >>> provideAdapter(MockAdapter)
    >>> root['ap3'] = ap3
    >>> len(global_apu)
    1
    >>> len(local_apu)
    0
    >>> del root['ap3']
    >>> len(global_apu)
    0
    >>> len(local_apu)
    0


XXX: test persistency?
