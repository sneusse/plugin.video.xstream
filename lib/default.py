# -*- coding: utf-8 -*-
import sys
import xstream

from xstream.lib import kodi
from xstream.lib.gui import Gui, MenuItem, PluginMenuItem
from xstream.lib.settings import Settings


def show_main_menu():
    gui = Gui()

    plugins = xstream.get_plugins()
    for plugin in plugins:
        gui.add_menu_entry(PluginMenuItem(plugin.name, 'main', id=plugin.id))

    gui.add_menu_entry(MenuItem('Meta Settings', 'meta_menu'))
    gui.generate_menu()


def show_plugin_menu(params):
    if 'plugin_id' not in params:
        return show_main_menu()

    plugin_class = xstream.get_plugin(params['plugin_id'])

    if plugin_class:
        plugin = plugin_class()
        if not plugin.call_func(params):
            return show_main_menu()
    else:
        return show_main_menu()

def show_meta_settings():
    import metahandler
    metahandler.display_settings()

def _generate_settings():
    settings = Settings()

    xstream.generate_plugin_settings(settings)

    settings.generate_xml()

MENU_MAP = {
    'main_menu': show_main_menu,
    'meta_menu': show_meta_settings,
    'plugin': show_plugin_menu,
}

def main(argv=None):
    if sys.argv: argv = sys.argv
    mode, params = kodi.parse_query(argv[2])

    _generate_settings()

    if mode not in MENU_MAP:
        mode = 'main_menu'
        params = None

    func = MENU_MAP[mode]

    print params

    if params:
        func(params)
    else:
        func()


if __name__ == '__main__':
    sys.exit(main())
