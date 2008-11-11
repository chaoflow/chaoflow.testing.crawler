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

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IGroupsPlugin

from zope.app.security.interfaces import IAuthentication
from zope.app.security.interfaces import PrincipalLookupError
from zope.component import getUtility
from zope.interface import implements


manage_addGroupsPluginForm = PageTemplateFile(
    '../www/GroupsPluginForm',
    globals(), __name__='manage_addGroupsPluginForm' )


def addGroupsPlugin( dispatcher, id, title=None, REQUEST=None ):
    """Add a paula.pasplugins GroupsPlugin to a PluggableAuthService.
    """
    plugin = GroupsPlugin(id, title)
    dispatcher._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'paula.pasplugins.GroupsPlugin+added.'
                            % dispatcher.absolute_url())


class GroupsPlugin(BasePlugin):
    """
    """
    security = ClassSecurityInfo()

    implements(IGroupsPlugin)

    meta_type = "Paula PAS Groups Plugin"

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    security.declarePrivate('getGroupsForPrincipal')
    def getGroupsForPrincipal(self, principal, request=None):
        """ principal -> ( group_1, ... group_N )

        o Return a sequence of group names to which the principal 
          (either a user or another group) belongs.

        o May assign groups based on values in the REQUEST object, if present
        """
        # get principal from pau
        pau = getUtility(IAuthentication)
        try:
            p = pau.getPrincipal(principal.getId())
        except PrincipalLookupError:
            return {}

        if not p:
            return {}

        # eventually we need to return allGroups from an
        # IGroupClousureAwarePrincipal
        return tuple(p.groups)


InitializeClass( GroupsPlugin)
