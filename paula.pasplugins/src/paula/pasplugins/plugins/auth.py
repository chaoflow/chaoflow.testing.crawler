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

import UserDict

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

#from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PluggableAuthService.interfaces.plugins \
        import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserAdderPlugin
from Products.PluggableAuthService.interfaces.plugins \
        import IUserEnumerationPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from zope.app.security.interfaces import IAuthentication
from zope.app.security.interfaces import PrincipalLookupError

from zope.interface import implements, alsoProvides
from zope.component import getUtility
from zope.publisher.interfaces import IRequest

from paula.pasplugins.tests.fake_pau_ap import FAKE_LOGIN

manage_addAuthenticationPluginForm = PageTemplateFile(
    '../www/AuthenticationPluginForm',
    globals(), __name__='manage_addAuthenticationPluginForm' )


def addAuthenticationPlugin( dispatcher, id, title=None, REQUEST=None ):
    """Add a paula.plonepas AuthenticationPlugin to a PluggableAuthService.
    """
    plugin = AuthenticationPlugin(id, title)
    dispatcher._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'paula.pasplugins.AuthenticationPlugin+added.'
                            % dispatcher.absolute_url())


class AuthenticationPlugin(BasePlugin):
    """
    """
    security = ClassSecurityInfo()

    implements(
            IAuthenticationPlugin,
            IUserEnumerationPlugin,
            IUserAdderPlugin,
#            IUserIntrospection,
            )

    meta_type = "Paula PAS Authentication Plugin"

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    # IAuthenticationPlugin
    #
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """ credentials -> (userid, login)

        o 'credentials' will be a mapping, as returned by IExtractionPlugin.

        o Return a tuple consisting of user ID (which may be different 
          from the login name) and login

        o If the credentials cannot be authenticated, return None.

        Mock principal

            >>> p = Mock(id = 'login')
        
        Mockup IPluggableAuthentication

            >>> au = Mock(authenticate = \\
            ...         lambda x : IRequest.providedBy(x) \\
            ...             and x.has_key('login') \\
            ...             and x.has_key('password') \\
            ...             and p,
            ...         alsoProvides=(IAuthentication,))
            >>> provideUtility(au, IAuthentication)

        our authentication plugin

            >>> ap = AuthenticationPlugin('ap')

        wrong credentials

            >>> creds = {}
            >>> creds['login'] = 'foo'
            >>> ap.authenticateCredentials(creds) is None
            True

        correct credentials

            >>> creds['password'] = 'foo'
            >>> ap.authenticateCredentials(creds)
            ('login', 'login')

        and otherway wrong creds

            >>> del creds['login']
            >>> ap.authenticateCredentials(creds) is None
            True
        """
        pau = getUtility(IAuthentication)

        # pau expects something providing request
        # our fake credentials plugin is fine with a mapping
        request = UserDict.UserDict(credentials)
        alsoProvides(request, IRequest)

        principal = pau.authenticate(request)
        if principal:
            return (principal.id, principal.id)

        #if credentials['login'] is 'adam':
        #    return ('adam', 'adam')

        return None

    # IUserAdderPlugin
    #
    security.declarePrivate( 'enumerateUsers' )
    def doAddUser(self, login, password):
        # if successful add return True


        return False

    # IUserEnumerationPlugin
    #
    security.declarePrivate( 'enumerateUsers' )
    def enumerateUsers( self
                      , id=None
                      , login=None
                      , exact_match=False
                      , sort_by=None
                      , max_results=None
                      , **kw
                      ):
        pau = getUtility(IAuthentication)

        #XXX: currently we only know exact match
        #if exact_match:
        if exact_match or not exact_match:
            #XXX: id and login are treated equal - fixme!
            try:
                principal = pau.getPrincipal( id or login)
            except PrincipalLookupError:
                return ({},)

            #XXX: do something with the data from the returned principal?!
            return ({
                    'id': login or id,
                    'login': login or id,
                    'pluginid': self.getId(),
                    },)

    # IUserIntrospection
    #
    #security.declarePrivate('getUserIds')
    #def getUserIds(self):
    #    return ('fakelogin',)

    # IUserIntrospection
    #
    #security.declarePrivate('getUserNames')
    #def getUserNames(self):
    #    return ('fakelogin',)

    # IUserIntrospection
    #
    #security.declarePrivate('getUsers')
    #def getUsers(self):
    #    """
    #    Return a list of users
#
#        XXX DON'T USE THIS, it will kill performance
#        """
#        uf = getToolByName(self, 'acl_users')
#        return tuple([uf.getUserById(x) for x in self.getUserIds()])


InitializeClass( AuthenticationPlugin)
