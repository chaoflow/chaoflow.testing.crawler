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

# only for testing purposes
#from paula.pasplugins.tests.fake_pau_ap import AUTHPLUG_NAME

def _setupPlugins(portal, out):
    """
    Install and prioritize the Paula PAS plug-ins.
    """
    uf = getToolByName(portal, 'acl_users')

    paula = uf.manage_addProduct['paula.pasplugins']
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
