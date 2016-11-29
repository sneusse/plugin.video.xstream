# -*- coding: utf-8 -*-
import os
import xbmcaddon

addon = xbmcaddon.Addon('plugin.video.xstream')

addon_path = addon.getAddonInfo('path').decode('utf-8')
settings_file = os.path.join(addon_path, 'resources', 'settings.xml')