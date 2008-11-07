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

# this should be moved from zope.app.authentication to zope.authentication
from zope.app.authentication.interfaces import ICredentialsPlugin
from zope.app.authentication.principalfolder import PrincipalInfo

from zope.app.container.contained import Contained
from zope.interface import implements, alsoProvides
from zope.component import getUtility
from zope.publisher.interfaces import IRequest

from paula.authentication.interfaces import IAuthProviders
from paula.authentication.interfaces import IAuthenticatorPlugin
from paula.authentication.interfaces import ILocalAuthenticatorPlugin
from paula.authentication.interfaces import ICredentialsFromMappingPlugin


class AuthenticatorPlugin(object):
    """Authenticate users with auth providers from an IAuthProviders
    
    May be registered globally, as only functionality is implemented.

        >>> import UserDict
        >>> apu = UserDict.UserDict()
        >>> alsoProvides(apu, IAuthProviders)
        >>> provideUtility(apu)

        >>> m = Mock(
        ...         id='login',
        ...         validate = lambda login=None,password=None: \\
        ...                 password == 'correct',
        ...         )

        >>> apu['login'] = m
        
        >>> ap = AuthenticatorPlugin()

        >>> p = ap.authenticateCredentials(None)
        >>> p is None
        True

        >>> credentials = {
        ...     'login': 'login',
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials = {
        ...     'password': 'correct',
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials = {
        ...     'login': 'wrong',
        ...     'password': 'correct',
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials['login'] = 'login'
        >>> p = ap.authenticateCredentials(credentials)
        >>> from zope.app.authentication.interfaces import IPrincipalInfo
        >>> IPrincipalInfo.providedBy(p)
        True
        >>> p.id
        'login'

        >>> credentials['password'] = 'wrong'
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True
    """
    implements(IAuthenticatorPlugin)

    def _getAPU(self):
        """
        """
        return getUtility(IAuthProviders)

    def authenticateCredentials(self, creds):
        try:
            if not (creds.has_key('login') and creds.has_key('password')):
                return None
        except AttributeError:
            return None
        
        # retrieve auth provider utility
        apu = self._getAPU()
        id = creds["login"]
        try:
            # retrieve auth provider for principal
            ap = apu[id]
        except KeyError:
            return None

        # use authprovider to verify credentials
        if not ap.validate(login=creds['login'],password=creds['password']):
            return None

        login = id
        title = description = u""
        return PrincipalInfo( id, login, title, description)

    def principalInfo(self, id):
        apu = self._getAPU()
        if not id in apu:
            return None
        login = id
        title = description = u""
        return PrincipalInfo( id, login, title, description)


class LocalAuthenticatorPlugin(
        AuthenticatorPlugin,
        Contained,
        ):
    """XXX: still not sure whether this could be the same as AP
    """
    implements(ILocalAuthenticatorPlugin)

#    def _getAPU(self):
#        """when doing this in the version above, I am getting a
#        ComponentLookupError...
#        """
#        return getUtility(IAuthProviders, context=getSite())


class CredentialsFromMappingPlugin(Contained):
    """Just returns a mapping it is passed

    Useful, if you use paula and PAU just for authentication but not for
    challenging, i.e./e.g. from PlonePAS you already get the credentials in a
    mapping and don't need to bother with challenging.

    May be registered globally, as only functionality is implemented.

        >>> cp = CredentialsFromMappingPlugin()
        >>> m = UserDict()
        >>> c = cp.extractCredentials(m)
        >>> c is m
        True
        >>> IRequest.providedBy(m)
        True
    """
    implements(ICredentialsFromMappingPlugin)
    
    def extractCredentials(self, mapping):
        """
        """
        # tune the mapping, PAU needs an IRequest to find its factories
        # If this does not work, better let the AttributeError go here, than
        # later in the getMultiAdapter lookup of PAU
        if not IRequest.providedBy(mapping):
            alsoProvides(mapping, IRequest)

        return mapping
    
    def challenge(self, request):
        pass # challenge is a no-op for this plugin
    
    def logout(self, request):
        pass # logout is a no-op for this plugin

