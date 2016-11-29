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
from lib.settings import Settings

def main():
    pass

def get_plugins(include_disabled=False):
    classes = SitePlugin.__class__.__subclasses__(SitePlugin)

    plugins = []

    for plugin in classes:
        if plugin.is_enabled or include_disabled:
            plugins.append(plugin)

    return plugins

def _generate_settings():
    settings = Settings()

    settings.create_category('30021')
    for plugin in get_plugins(include_disabled=True):
        addon_id = 'plugin_%s' % plugin.id
        settings.create_lsep(plugin.name)
        settings.create_input_bool(addon_id, '30050', 'true')
        settings.set_prefix(addon_id)
        plugin.custom_settings(settings)
        settings.clear_prefix()

    settings.generate_xml()