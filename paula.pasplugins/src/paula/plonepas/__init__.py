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


from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin

from paula.plonepas.plugins import auth
from paula.plonepas.plugins import groups
from paula.plonepas.plugins import properties


def initialize(context):
    """
    """
    registerMultiPlugin(auth.AuthenticationPlugin.meta_type)

    context.registerClass(
            auth.AuthenticationPlugin,
            permission = add_user_folders,
            #icon='www/paula.gif',
            constructors = (
                    auth.manage_addAuthenticationPluginForm,
                    auth.addAuthenticationPlugin,
                    ),
            visibility = None,
            )


    registerMultiPlugin(groups.GroupsPlugin.meta_type)

    context.registerClass(
            groups.GroupsPlugin,
            permission = add_user_folders,
            #icon='www/paula.gif',
            constructors = (
                    groups.manage_addGroupsPluginForm,
                    groups.addGroupsPlugin,
                    ),
            visibility = None,
            )


    registerMultiPlugin(properties.PropertiesPlugin.meta_type)

    context.registerClass(
            properties.PropertiesPlugin,
            permission = add_user_folders,
            #icon='www/paula.gif',
            constructors = (
                    properties.manage_addPropertiesPluginForm,
                    properties.addPropertiesPlugin,
                    ),
            visibility = None,
            )
