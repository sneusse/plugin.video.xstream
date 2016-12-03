# -*- coding: utf-8 -*-
import os
import sys

from xstream.lib import kodi

addon_path = kodi.get_path()
addon_handle = int(sys.argv[1])
profile_path = kodi.translate_path(kodi.get_profile())
settings_file = os.path.join(addon_path, 'resources', 'settings.xml')