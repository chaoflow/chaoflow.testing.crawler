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

from zope.interface import Interface
from zope.schema import TextLine
from zope.app.authentication.interfaces import IAuthenticatorPlugin as IPauAP


class IAuthenticatorPlugin(IPauAP):
    """A paula authenticator plugin for PAU
    """

class ILocalAuthenticatorPlugin(IAuthenticatorPlugin):
    """A context-aware paula authenticator plugin for PAU
    """

class IPrincipalId(Interface):
    """A principals unique id
    """
    id = TextLine(
            title=u"Id",
            description=u"The unique principal id.",
            required=True,
            )


class IAuthProvider(IPrincipalId):
    """
    """
    def validate(login=u"", password=u""):
        """validates the password against a stored password
        """


class IAuthProviders(Interface):
    """auth providers for authenticatable principals known to paula
    """
    def __getitem__(id):
        """returns a paula IAuthProvider object for the principal id
        """
