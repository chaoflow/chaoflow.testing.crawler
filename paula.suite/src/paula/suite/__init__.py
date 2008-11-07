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

from zope.app.authentication import principalfolder
from zope.app.authentication.authentication import PluggableAuthentication
from zope.app.authentication.interfaces import IPluggableAuthentication

from zope.app.security.interfaces import IAuthentication
from zope.app.folder import Folder

from zope.component import getSiteManager, provideAdapter

from paula.authentication import LocalAuthenticatorPlugin
from paula.authentication import CredentialsFromMappingPlugin
from paula.authentication.interfaces import ILocalAuthenticatorPlugin
from paula.authentication.interfaces import ICredentialsFromMappingPlugin

from paula.authutil import RWAuthProviders
from paula.authutil.interfaces import IRWAuthProviders

from paula.proputil import RWPropertyProviders
from paula.proputil.interfaces import IRWPropertyProviders

from config import PAULA_AUTHPLUGIN_NAME
from config import PAULA_CREDPLUGIN_NAME

from persistent import Persistent

#def createPaulaSuite(container=None, create_pau=False, create_credplug=False):
def createPaulaSuite(container, create_pau=False, create_credplugin=False,
        ContainerType=None):
    """Creates paula components in the given container and registers them
    """
    sm = getSiteManager(container)

    if create_pau and not 'paula_pau' in container:
        try:
            from OFS.SimpleItem import Item
            import Acquisition
            import AccessControl.Role
        except ImportError:
            MyPluggableAuthentication = PluggableAuthentication
        else:
            class MyPluggableAuthentication(
                     PluggableAuthentication,
                     Item,
                     Acquisition.Implicit,
                     AccessControl.Role.RoleManager,
                     ):
                def __init__(self):
                    super(MyPluggableAuthentication, self).__init__()
        pau = MyPluggableAuthentication()
        container['paula_pau'] = pau

        # register PAU as IAuthentication and IPluggableAuthentication
        sm = getSiteManager(container)
        sm.registerUtility(pau, IAuthentication)
        sm.registerUtility(pau, IPluggableAuthentication)

        # register principal factories needed by PAU
        # XXX: bug in zope.app.authentication, we need to register globally
        #sm.registerAdapter(principalfolder.AuthenticatedPrincipalFactory)
        #sm.registerAdapter(principalfolder.FoundPrincipalFactory)
        provideAdapter(principalfolder.AuthenticatedPrincipalFactory)
        provideAdapter(principalfolder.FoundPrincipalFactory)

    pau = sm.getUtility(IPluggableAuthentication)

    # Paula's PAU AuthenticatorPlugin
    if not 'paula_authplugin' in container:
        authplugin = LocalAuthenticatorPlugin()
        container['paula_authplugin'] = authplugin
        sm.registerUtility( authplugin,
                ILocalAuthenticatorPlugin,
                name=PAULA_AUTHPLUGIN_NAME,
                )
        pau.authenticatorPlugins += (PAULA_AUTHPLUGIN_NAME,)
    
    if create_credplugin and not 'paula_credplugin' in container:
        credplugin = CredentialsFromMappingPlugin()
        container['paula_credplugin'] = credplugin
        sm.registerUtility( credplugin,
                ICredentialsFromMappingPlugin,
                name=PAULA_CREDPLUGIN_NAME,
                )
        pau.credentialsPlugins += (PAULA_CREDPLUGIN_NAME,)

    if not 'authutil' in container:
        authutil = RWAuthProviders()
        container['paula_authutil'] = authutil
        sm.registerUtility( authutil, IRWAuthProviders)

    if not 'paula_proputil' in container:
        proputil = RWPropertyProviders()
        container['paula_proputil'] = proputil
        sm.registerUtility( proputil, IRWPropertyProviders)
