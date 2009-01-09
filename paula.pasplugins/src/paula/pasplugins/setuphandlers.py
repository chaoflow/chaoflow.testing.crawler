"""
"""
__author__ = "Florian Friesdorf <flo@chaoflow.net>"
__docformat__ = "plaintext"

from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.interfaces.plugins \
     import IAuthenticationPlugin
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from zope.app.security.interfaces import IAuthentication
from zope.component import getUtility

from paula.pasplugins.plugins.auth import paula_auth_ifs
from paula.pasplugins.plugins.groups import paula_groups_ifs
from paula.pasplugins.plugins.properties import paula_properties_ifs

# only for testing purposes
#from paula.pasplugins.tests.fake_pau_ap import AUTHPLUG_NAME

def _setupPlugins(portal, out):
    """
    Install and prioritize the Paula PAS plug-ins.
    """
    uf = getToolByName(portal, 'acl_users')

    paula = uf.manage_addProduct['paula.pasplugins']
    plugins = uf.plugins

    def _move_to_top(interface, name):
        while not plugins.listPlugins(
                interface,
                )[0][0] == name:
            plugins.movePluginsUp(interface, [name])

    existing = uf.objectIds()

    if 'paula_auth' not in existing:
        paula.addAuthenticationPlugin('paula_auth')
        print >> out, "Added Paula PAS Authentication Plugin."
        activatePluginInterfaces(portal, 'paula_auth', out)
        for x in paula_auth_ifs:
            _move_to_top(x, 'paula_auth')

    if 'paula_properties' not in existing:
        paula.addPropertiesPlugin('paula_properties')
        print >> out, "Added Paula PAS Properties Plugin."
        activatePluginInterfaces(portal, 'paula_properties', out)
        for x in paula_properties_ifs:
            _move_to_top(x, 'paula_properties')

    if 'paula_groups' not in existing:
        paula.addGroupsPlugin('paula_groups')
        print >> out, "Added Paula PAS Groups Plugin."
        activatePluginInterfaces(portal, 'paula_groups', out)
        for x in paula_groups_ifs:
            _move_to_top(x, 'paula_groups')

    credplugname = 'Paula: PAU CredentialsFromMappingPlugin'
    pau = getUtility(IAuthentication)
    if credplugname not in pau.credentialsPlugins:
        pau.credentialsPlugins = tuple(
                list(pau.credentialsPlugins) + [credplugname]
                )
        # only for testing purposes
        #pau.authenticatorPlugins = (AUTHPLUG_NAME,)


def setupPlugins(context):
    """initialize paula plugins
    """
    if context.readDataFile('paula-pasplugins-setup-plugins.txt') is None:
        return

    portal = context.getSite()
    out = StringIO()
    _setupPlugins(portal, out)
    logger = context.getLogger("plugins")
    logger.info(out.getvalue())
