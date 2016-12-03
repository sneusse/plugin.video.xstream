# -*- coding: utf-8 -*-
import urllib
import urlparse
import sys

import xbmc
import xbmcaddon
import xbmcplugin


addon = xbmcaddon.Addon('plugin.video.xstream')

def get_path():
    return addon.getAddonInfo('path').decode('utf-8')

def get_profile():
    return addon.getAddonInfo('profile').decode('utf-8')

def translate_path(path):
    return xbmc.translatePath(path).decode('utf-8')

def get_plugin_url(queries):
    try:
        query = urllib.urlencode(queries)
    except UnicodeEncodeError:
        for k in queries:
            if isinstance(queries[k], unicode):
                queries[k] = queries[k].encode('utf-8')
        query = urllib.urlencode(queries)

    return sys.argv[0] + '?' + query

def parse_query(query):
    mode = 'main_menu'
    params = {}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if key == 'mode':
            mode = queries[key][0]
            continue

        if len(queries[key]) == 1:
            params[key] = queries[key][0]
        else:
            params[key] = queries[key]
    return mode, params

def show_settings():
    try:
        xbmcplugin.openSettings(int(sys.argv[1]))
    except:
        pass

def get_setting(name, default=''):
    try:
        value = str(xbmcplugin.getSetting(int(sys.argv[1]), name))
        if value.lower() == 'true' or value.lower() == 'false':
            return value.lower() == 'true'
        return value
    except:
        return default

def set_setting(name, value):
    try:
        xbmcplugin.setSetting(int(sys.argv[1]), name, value)
        return True
    except:
        return False

def get_localized_string(self, name):
    try:
        return xbmc.getLocalizedString(name)
    except:
        return ''