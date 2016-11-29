# -*- coding: utf-8 -*-
import sys

import xbmc
import xbmcaddon
import xbmcplugin

addon = xbmcaddon.Addon('plugin.video.xstream')


def show_settings():
    try:
        xbmcplugin.openSettings(sys.argv[0])
    except:
        pass

def get_setting(name, default=''):
    try:
        return xbmcplugin.getSetting(sys.argv[0], name)
    except:
        return default

def set_setting(name, value):
    try:
        xbmcplugin.setSetting(sys.argv[0], name, value)
        return True
    except:
        return False

def get_localized_string(self, name):
    try:
        return xbmc.getLocalizedString(name)
    except:
        return ''