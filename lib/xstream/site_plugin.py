# -*- coding: utf-8 -*-
import abc
import json

from xstream.lib import kodi
from xstream.lib.gui.menu_handler import MenuHandler
from xstream.lib.net import Net


class SitePlugin(MenuHandler):
    __metaclass__ = abc.ABCMeta

    id = ''
    name = ''
    version = 0.0

    def __init__(self):
        self.net = Net()
        super(SitePlugin, self).__init__(self.id)

    def call_func(self, params):
        func_name = params['plugin_func'] if 'plugin_func' in params else 'main'
        func_params = json.loads(params['plugin_params']) if 'plugin_params' in params else None

        if not hasattr(self, func_name):
            return False

        plugin_func = getattr(self, func_name)

        if func_params:
            plugin_func(**func_params)
        else:
            plugin_func()

        self.generate_menu()

        return True

    @classmethod
    def custom_settings(cls, settings):
        pass

    @abc.abstractmethod
    def main(self):
        return NotImplementedError

    @classmethod
    def is_enabled(cls):
        return kodi.get_setting('plugin_%s' % cls.id, False)