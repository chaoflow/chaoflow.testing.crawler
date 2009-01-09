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

from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PlonePAS.interfaces.capabilities import IDeleteCapability
from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability
from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement

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


paula_auth_ifs = (
            IAuthenticationPlugin,
            IUserAdderPlugin,
            IUserEnumerationPlugin,
            IUserManagement,
#            IUserIntrospection,
            )

class AuthenticationPlugin(BasePlugin):
    """
    """
    implements(
            IDeleteCapability,
            IPasswordSetCapability,
            *paula_auth_ifs
            )

    meta_type = "Paula PAS Authentication Plugin"

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    # IAuthenticationPlugin
    #
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
    def doAddUser(self, login, password):
        """ Add a user record to a User Manager, with the given login
            and password

        o Return a Boolean indicating whether a user was added or not
        """
        pau = getUtility(IAuthentication)
        if pau.addUser(login, password):
            return True

        return False


    # IDeleteCapability
    #
    def allowDeletePrincipal(self, id):
        """True iff this plugin can delete a certain user/group.
        """
        #XXX: We need to check with PAU whether we can delete the principal
        pau = getUtility(IAuthentication)
        return pau.allowDeletePrincipal(id)
        
    # IPasswordSetCapability
    #
    def allowPasswordSet(self, id):
        """True iff this plugin can set the password of a certain user.
        """
        pau = getUtility(IAuthentication)
        return pau.allowPasswordSet(id)

    # IUserManagamenet
    #
    def doChangeUser(self, login, password, **kws):
        """
        Change a user's password (differs from role) roles are set in
        the pas engine api for the same but are set via a role
        manager)
        """
        pau = getUtility(IAuthentication)
        if not pau.doChangeUser(login, password, **kws):
            # maybe should be moved to the PAU auth plugins
            raise RuntimeError

    def doDeleteUser(self, login):
        """
        Remove a user record from a User Manager, with the given login
        and password

        o Return a Boolean indicating whether a user was removed or
          not
        """
        pau = getUtility(IAuthentication)
        return pau.delPrincipal(login)

    # IUserEnumerationPlugin
    #
    def enumerateUsers( self
                      , id=None
                      , login=None
                      , exact_match=False
                      , sort_by=None
                      , max_results=None
                      , **kw
                      ):
        pau = getUtility(IAuthentication)

        if exact_match:
            #XXX: id and login are treated equal - fixme!
            try:
                principal = pau.getPrincipal( id or login)
            except PrincipalLookupError:
                return ()

            #XXX: do something with the data from the returned principal?!
            return ({
                    'id': login or id,
                    'login': login or id,
                    'pluginid': self.getId(),
                    },)

        # XXX: no exact_match, we need to search for the user in PAU

#    # IUserIntrospection
#    #
#    def getUserIds(self):
#        # called eg when going into the memberdata tool contents
#        return ('fakelogin',)
#
#    # IUserIntrospection
#    #
#    def getUserNames(self):
#        return ('fakelogin',)
#
#    # IUserIntrospection
#    #
#    def getUsers(self):
#        """
#        Return a list of users
#
#        XXX DON'T USE THIS, it will kill performance
#        """
#        uf = getToolByName(self, 'acl_users')
#        return tuple([uf.getUserById(x) for x in self.getUserIds()])


InitializeClass( AuthenticationPlugin)
