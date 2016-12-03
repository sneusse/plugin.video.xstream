# -*- coding: utf-8 -*-
import sys

import xbmc
import xbmcgui
import xbmcplugin

from xstream.lib import kodi, utils


class Gui:
    _menu_entries = []
    _media_type = None

    def __init__(self):
        self._plugin_handle = int(sys.argv[1])
        self._meta_update = True

    @property
    def meta_update(self):
        return self._meta_update

    @meta_update.setter
    def meta_update(self, value):
        self._meta_update = value

    def add_menu_entry(self, menu_entry):
        self._menu_entries.append(menu_entry)

    def generate_menu(self):
        for item in self._menu_entries:
            url = kodi.get_plugin_url(item.get_dict())
            list_item = xbmcgui.ListItem(item.title)

            if hasattr(item, 'info_item') and item.info_item:
                info_item = item.info_item
                art_dict = {}

                if self.meta_update:
                    art_dict = self._get_metadata(info_item)

                if self._media_type:
                    info_item.mediatype = self._media_type

                list_item.setArt(art_dict)
                list_item.setInfo('video', info_item.__dict__)

            xbmcplugin.addDirectoryItem(self._plugin_handle, url, list_item, isFolder=True, totalItems=0)

        self._set_end_of_directory()

    def set_view(self, content='movies'):
        '''
        set the listing to a certain content, makes special views available
        sets view to the viewID which is selected in xStream settings

        see http://mirrors.xbmc.org/docs/python-docs/stable/xbmcplugin.html#-setContent
        (seasons is also supported but not listed)
        '''
        content = content.lower()
        view_mapping = {
            'files': None,
            'songs': None,
            'artists': None,
            'albums': None,
            'movies': 'movie',
            'tvshows': 'tvshow',
            'seasons': 'season',
            'episodes': 'episode',
            'musicvideos': 'musicvideo'
        }

        if content in view_mapping:
            if view_mapping[content]:
                self._media_type = view_mapping[content]
            xbmcplugin.setContent(self._plugin_handle, content)

    def _add_folder(self):
        if xbmc.abortRequested:
            self._set_end_of_directory(False)
            raise RuntimeError('UserAborted')

    def _set_end_of_directory(self, success=True, updateListing=False):
        xbmcplugin.endOfDirectory(self._plugin_handle, success, updateListing)

    def _get_metadata(self, info_item):
        meta_handler = utils.get_metahandler()

        if not meta_handler:
            return

        art_types = ['thumb', 'poster', 'banner', 'fanart', 'clearart', 'clearlogo', 'landscape', 'icon']
        art_dict = {}

        if not info_item.season:
            metadata = meta_handler.get_meta('tvshow', info_item.tvshowtitle, info_item.code, year=info_item.year)
        elif not info_item.episode:
            metadata = meta_handler.get_seasons(info_item.tvshowtitle, info_item.code, info_item.season)
        else:
            metadata = meta_handler.get_episode_meta(info_item.tvshowtitle, info_item.code, info_item.season,
                                                     info_item.episode)

        for key in metadata:
            str_key = str(key).lower()
            if hasattr(info_item, str_key):
                setattr(info_item, str_key, metadata[key])
            if str_key in art_types:
                art_dict[str_key] = metadata[key]

        return art_dict



