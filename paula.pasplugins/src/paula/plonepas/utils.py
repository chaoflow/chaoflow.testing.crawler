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

from OFS.SimpleItem import SimpleItem

from paula.authentication import LocalAuthenticatorPlugin as \
        AuthenticatorPluginBase
from paula.authentication import CredentialsFromMappingPlugin as \
        CredentialsFromMappingPluginBase
from paula.authutil import RWAuthProviders as \
        RWAuthProvidersBase
from paula.proputil import RWPropertyProviders as \
        RWPropertyProvidersBase
from paula.grouputil import RWMemberships as \
        RWMembershipsBase
from zope.app.authentication.authentication import PluggableAuthentication as \
        PluggableAuthenticationBase


class PluggableAuthentication(SimpleItem, PluggableAuthenticationBase):
    """
    """
    authenticatorPlugins = ('Paula PAU AuthenticatorPlugin',)
    credentialsPlugins = ('Paula PAU CredentialsFromMappingPlugin',)

    def __init__(self):
        super(PluggableAuthentication, self).__init__()


class AuthenticatorPlugin(SimpleItem, AuthenticatorPluginBase):
    """
    """
    def __init__(self):
        super(AuthenticatorPlugin, self).__init__()


class CredentialsFromMappingPlugin(SimpleItem, CredentialsFromMappingPluginBase):
    """
    """
    def __init__(self):
        super(CredentialsFromMappingPlugin, self).__init__()


class RWAuthProviders(SimpleItem, RWAuthProvidersBase):
    """
    """
    def __init__(self):
        super(RWAuthProviders, self).__init__()


class RWPropertyProviders(SimpleItem, RWPropertyProvidersBase):
    """
    """
    def __init__(self):
        super(RWPropertyProviders, self).__init__()


class RWMemberships(SimpleItem, RWMembershipsBase):
    """
    """
    def __init__(self):
        super(RWMemberships, self).__init__()
