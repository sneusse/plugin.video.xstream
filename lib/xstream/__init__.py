# -*- coding: utf-8 -*-
"""
    xStream Addon for Kodi/XBMC
    Copyright (C) 2016 Seberoth

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from xstream.site_plugin import SitePlugin
from xstream.lib.settings import Settings

from xstream.plugins import *


def get_plugin(id):
    plugins = get_plugins()

    for plugin in plugins:
        if plugin.id == id:
            return plugin

    return None


def get_plugins(include_disabled=False):
    classes = SitePlugin.__class__.__subclasses__(SitePlugin)

    plugins = []

    for plugin in classes:
        if plugin.is_enabled or include_disabled:
            plugins.append(plugin)

    return plugins

def generate_plugin_settings(settings):
    settings.create_category('30021')

    for plugin in get_plugins(include_disabled=True):
        plugin_id = 'plugin_%s' % plugin.id
        settings.create_lsep(plugin.name)
        settings.create_input_bool(plugin_id, '30050', 'true')
        settings.set_prefix(plugin_id)
        plugin.custom_settings(settings)
        settings.clear_prefix()
