paula.plonepas package readme
=============================

Set things up (thx optilux)
---------------------------

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see error messages properly.

    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()

We then turn off the various portlets, because they sometimes duplicate links
and text (e.g. the navtree, the recent recent items listing) that we wish to
test for in our own views. Having no portlets makes things easier.

    >>> from zope.component import getMultiAdapter, getUtility
    >>> from plone.portlets.interfaces import IPortletManager
    >>> from plone.portlets.interfaces import IPortletAssignmentMapping

    >>> left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
    >>> left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
    >>> for name in left_assignable.keys():
    ...     del left_assignable[name]

    >>> right_column = getUtility(IPortletManager, name=u"plone.rightcolumn")
    >>> right_assignable = getMultiAdapter((self.portal, right_column), IPortletAssignmentMapping)
    >>> for name in right_assignable.keys():
    ...     del right_assignable[name]


Start testing
-------------

Make sure all components have been registered

    >>> from zope.app.security.interfaces import IAuthentication
    >>> from paula.authentication.interfaces import ILocalAuthenticatorPlugin
    >>> from paula.authentication.interfaces import \
    ...         ICredentialsFromMappingPlugin
    >>> from paula.authentication.interfaces import IAuthProviders
    >>> from paula.properties.interfaces import IPropertyProviders
    >>> from paula.groups.interfaces import IMemberships

    >>> pau = getUtility(IAuthentication, context=portal)
    >>> pau.__parent__ = portal
    >>> pau
    <PluggableAuthentication at /plone/>
    >>> ap = getUtility(ILocalAuthenticatorPlugin, context=portal, 
    ...         name='Paula PAU AuthenticatorPlugin')
    >>> ap.__parent__ = portal
    >>> ap
    <AuthenticatorPlugin at /plone/>
    >>> cp = getUtility(ICredentialsFromMappingPlugin, context=portal, 
    ...         name='Paula PAU CredentialsFromMappingPlugin')
    >>> cp.__parent__ = portal
    >>> cp
    <CredentialsFromMappingPlugin at /plone/>
    >>> apu = getUtility(IAuthProviders, context=portal)
    >>> apu.__parent__ = portal
    >>> apu
    <RWAuthProviders at /plone/>
    >>> ppu = getUtility(IPropertyProviders, context=portal)
    >>> ppu.__parent__ = portal
    >>> ppu
    <RWPropertyProviders at /plone/>
    >>> mu = getUtility(IMemberships, context=portal)
    >>> mu.__parent__ = portal
    >>> mu
    <RWMemberships at /plone/>


Add a user to the site

    >>> from zope.component import createObject
    >>> user = createObject('paula.ploneexamples.MinimalPloneUser', "user")
    >>> user.title = u"user"
    >>> user.password = u'password'
    >>> user.email = u"foo@bar.com"
    >>> user.realname = u"Foo Bar"
    >>> portal['user'] = user

credentials for the user, for PAU/Paula testing

    >>> from zope.publisher.interfaces import IRequest
    >>> pau_req = UserDict(login="user", password="password")
    >>> alsoProvides(pau_req, IRequest)


Add groups

    >>> g1 = createObject('paula.ploneexamples.BasicGroup', 'g1')
    >>> g1.title = 'g1'
    >>> g1.members = ('user',)

    >>> g2 = createObject('paula.ploneexamples.BasicGroup', 'g2')
    >>> g2.title = 'g2'
    >>> g2.members = ('g1',)
    
    >>> portal['g1'] = g1
    >>> portal['g2'] = g2


Test PAU/Paula subsystem

    >>> principal = pau.authenticate(pau_req)
    >>> principal
    Principal('user')

    >>> principal.email
    u'foo@bar.com'
    >>> principal.realname
    u'Foo Bar'

    >>> principal.groups
    ['g1']


Paula PAS auth plugin

    >>> p = portal.acl_users.paula_auth.authenticateCredentials(pau_req)
    >>> p
    ('user', 'user')

make a plone user

    >>> from Products.PlonePAS.plugins.ufactory import PloneUser
    >>> pu = PloneUser(p[1])
    >>> pu
    <PloneUser 'user'>

Paula PAS properties plugin

    >>> psheet = portal.acl_users.paula_properties.getPropertiesForUser(pu)
    >>> psheet.propertyItems()
    [('email', u'foo@bar.com'), ('realname', u'Foo Bar')]
    
Paula PAS group plugin

    >>> portal.acl_users.paula_groups.getGroupsForPrincipal(pu)
    ('g1',)


try to authenticate

    >>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
    >>> browser.getControl(name='__ac_name').value = u"user"
    >>> browser.getControl(name='__ac_password').value = u"wrong"
    >>> browser.getControl(name='submit').click()
    >>> 'Login failed' in browser.contents
    True

    >>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
    >>> browser.getControl(name='__ac_name').value = u"user"
    >>> browser.getControl(name='__ac_password').value = u"password"
    >>> browser.getControl(name='submit').click()
    >>> 'Login failed' in browser.contents
    False
