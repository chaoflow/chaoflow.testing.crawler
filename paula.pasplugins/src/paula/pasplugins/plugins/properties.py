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


from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.sheet import MutablePropertySheet

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IPropertiesPlugin

from zope.app.authentication.interfaces import IPluggableAuthentication
from zope.app.security.interfaces import PrincipalLookupError
from zope.component import getUtility
from zope.interface import alsoProvides, implements

from paula.pau_addons.interfaces import IPropertyInterface


manage_addPropertiesPluginForm = PageTemplateFile(
    '../www/PropertiesPluginForm',
    globals(), __name__='manage_addPropertiesPluginForm' )


def addPropertiesPlugin( dispatcher, id, title=None, REQUEST=None ):
    """Add a paula.plonepas PropertiesPlugin to a PluggableAuthService.
    """
    plugin = PropertiesPlugin(id, title)
    dispatcher._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'paula.plonepas.PropertiesPlugin+added.'
                            % dispatcher.absolute_url())


class PropertiesPlugin(BasePlugin):
    """
    """
    security = ClassSecurityInfo()

    implements(IPropertiesPlugin)

    meta_type = "Paula PAS Properties Plugin"

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """ user -> {}

        o User will implement IPropertiedUser.

        o Plugin should return a dictionary or an object providing
          IPropertySheet.

        o Plugin may scribble on the user, if needed (but must still
          return a mapping, even if empty).

        o May assign properties based on values in the REQUEST object, if
          present

        Create a sophisticated mock principal

            >>> from zope.interface import Interface, Attribute

        property interfaces 

            >>> class IA(Interface):
            ...     id = Attribute('id')
            ...     a1 = Attribute("a1")
            ...     a2 = Attribute("a2")

            >>> class IB(Interface):
            ...     b1 = Attribute("b1")

            >>> alsoProvides(IA, IPropertyInterface)
            >>> alsoProvides(IB, IPropertyInterface)
            >>> IPropertyInterface.providedBy(IA)
            True
            >>> IPropertyInterface.providedBy(IB)
            True
            
        and the mock principal

            >>> class MockPrincipal(object):
            ...     implements(IA,IB)
            ...     id = 'login'
            ...     a1 = 1
            ...     a2 = 2
            ...     b1 = 1
            ...     c1 = 'will not show up'
        
            >>> p = MockPrincipal()

        Mockup IPluggableAuthentication

            >>> from zope.component import provideUtility
            >>> au = Mock(getPrincipal = lambda x : x == "login" and p)
            >>> alsoProvides(au, IPluggableAuthentication)
            >>> provideUtility(au, IPluggableAuthentication)

        our property plugin

            >>> pp = PropertiesPlugin('pp')

        a mockup plone user

            >>> ploneuser = Mock(getId = lambda : u"login")
            >>> psheet = pp.getPropertiesForUser(ploneuser)
            >>> psheet.getId()
            'pp'
            >>> psheet.propertyIds()
            ['a1', 'a2', 'b1']
            >>> psheet.propertyValues()
            [1, 2, 1]

        and for a non-existing user

            >>> ploneuser = Mock(getId = lambda : u"foo")
            >>> pp.getPropertiesForUser(ploneuser)
            {}
        """
        # get principal from pau
        pau = getUtility(IPluggableAuthentication)
        try:
            principal = pau.getPrincipal(user.getId())
        except PrincipalLookupError:
            return {}

        if not principal:
            return {}

        # create property dictionary from all attributes, which belong to
        # property schemas
        properties = {}
        for schema in list(principal.__provides__):
            if IPropertyInterface.providedBy(schema):
                for name in list(schema):
                    properties[name] = getattr(principal, name)

        if properties.has_key('id'):
            del properties['id']
        
        return MutablePropertySheet(self.id, **properties)

InitializeClass( PropertiesPlugin)
