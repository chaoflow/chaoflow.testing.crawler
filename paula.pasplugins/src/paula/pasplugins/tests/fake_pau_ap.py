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
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.principalfolder import PrincipalInfo

from zope.interface import implements

FAKE_LOGIN = 'fakelogin'
FAKE_PASSWORD = 'fakepassword'


class AuthenticatorPlugin(object):
    """Authenticate a fixed fake user

        >>> ap = AuthenticatorPlugin()

        >>> p = ap.authenticateCredentials(None)
        >>> p is None
        True

        >>> credentials = {
        ...     'login': FAKE_LOGIN,
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials = {
        ...     'password': FAKE_PASSWORD,
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials = {
        ...     'login': FAKE_LOGIN+'wrong',
        ...     'password': FAKE_PASSWORD,
        ...     }
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True

        >>> credentials['login'] = FAKE_LOGIN
        >>> p = ap.authenticateCredentials(credentials)
        >>> from zope.app.authentication.interfaces import IPrincipalInfo
        >>> IPrincipalInfo.providedBy(p)
        True
        >>> p.id == FAKE_LOGIN
        True

        >>> credentials['password'] = FAKE_PASSWORD+'wrong'
        >>> p = ap.authenticateCredentials(credentials)
        >>> p is None
        True
    """
    implements(IAuthenticatorPlugin)

    def authenticateCredentials(self, creds):
        try:
            if not (creds.has_key('login') and creds.has_key('password')):
                return None
        except AttributeError:
            return None

        if not (creds['login'] == FAKE_LOGIN
                and creds['password'] == FAKE_PASSWORD):
            return None
        
        id = FAKE_LOGIN
        login = id
        title = description = u"I am a fake user"
        return PrincipalInfo( id, login, title, description)

    def principalInfo(self, id):
        if not id == FAKE_LOGIN:
            return None

        login = id
        title = description = u"I am a fake user"
        return PrincipalInfo( id, login, title, description)
