# -*- coding: utf-8 -*-
from xstream.lib.gui import *


class MenuHandler(object):
    def __init__(self, id):
        self._id = id
        self._gui = Gui()

    def _add_menu_entry(self, link_title, func, info_item=None, params=None):
        self._gui.add_menu_entry(PluginMenuItem(link_title, func, info_item, params, self._id))

    def _set_view(self, view_type):
        self._gui.set_view(view_type)

    def generate_menu(self):
        self._gui.generate_menu()