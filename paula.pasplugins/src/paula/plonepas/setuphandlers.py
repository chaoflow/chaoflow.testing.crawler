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

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins \
     import IAuthenticationPlugin

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from plone.app.content.container import Container

#from zope.component import getUtility

from zope.app.authentication.interfaces import IPluggableAuthentication
from paula.authentication.interfaces import ILocalAuthenticatorPlugin
from paula.authentication.interfaces import ICredentialsFromMappingPlugin
from paula.authentication.interfaces import IAuthProviders
from paula.groups.interfaces import IMemberships
from paula.properties.interfaces import IPropertyProviders

from paula import suite


def _setupPlugins(portal, out):
    """
    Install and prioritize the Paula PAS plug-ins.
    """
    uf = getToolByName(portal, 'acl_users')

    paula = uf.manage_addProduct['paula.plonepas']
    existing = uf.objectIds()

    if 'paula_auth' not in existing:
        paula.addAuthenticationPlugin('paula_auth')
        print >> out, "Added Paula PAS Authentication Plugin."
        activatePluginInterfaces(portal, 'paula_auth', out)

        #plugins = uf.plugins
        #plugins.movePluginsUp(IAuthenticationPlugin, ['paula'])

    if 'paula_properties' not in existing:
        paula.addPropertiesPlugin('paula_properties')
        print >> out, "Added Paula PAS Properties Plugin."
        activatePluginInterfaces(portal, 'paula_properties', out)

    if 'paula_groups' not in existing:
        paula.addGroupsPlugin('paula_groups')
        print >> out, "Added Paula PAS Groups Plugin."
        activatePluginInterfaces(portal, 'paula_groups', out)


def setupPlugins(context):
    """initialize paula plugins
    """
    if context.readDataFile('paula-plonepas-setup-plugins.txt') is None:
        return

    portal = context.getSite()
    out = StringIO()
    _setupPlugins(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())


def _createPaulaSuite(portal, out):
    """
    """
    #suite.createPaulaSuite(portal, create_pau=True, create_credplugin=True,
    #        ContainerType=Container)
#    for x, name in (
#            (IPluggableAuthentication,
#                    ''),
#            (ILocalAuthenticatorPlugin,
#                    'Paula PAU AuthenticatorPlugin'),
#            (ICredentialsFromMappingPlugin, 
#                    'Paula PAU CredentialsFromMappingPlugin'),
#            (IAuthProviders,
#                    ''),
#            (IPropertyProviders,
#                    ''),
#            (IMemberships,
#                    '')):
#        util = getUtility(x, name=name, context=portal)
#        if not util.__parent__:
#            util.__parent__ = portal
#    pau = getUtility(IPluggableAuthentication, context=portal)
#    # these three don't work ?! - hardcoded now in utils.py
#    # probably something about persistency
#    pau.authenticatorPlugins = ('Paula PAU AuthenticatorPlugin',)
#    pau.credentialsPlugins = ('Paula PAU CredentialsFromMappingPlugin',)
#    pau.abcdef = 1
    print >> out, "Added Paula Suite to Portal."

def createPaulaSuite(context):
    """
    """
    if context.readDataFile('paula-plonepas-create-paula-suite.txt') is None:
        return

    portal = context.getSite()
    out = StringIO()
    _createPaulaSuite(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())

