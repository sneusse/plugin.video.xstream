# -*- coding: utf-8 -*-
import json
import xbmcgui

from xstream.site_plugin import SitePlugin
from xstream.lib import logger
from xstream.lib.gui.info_item import VideoInfoItem

from .api import *


class BurningSeriesOrgPlugin(SitePlugin):
    id = 'burning_series_org'
    name = 'BurningSeries'

    URL_MAIN = 'https://www.bs.to/api/'
    URL_COVER = 'https://s.bs.to/img/cover/%s.jpg|encoding=gzip'

    def main(self):
        self._add_menu_entry('Alle Serien', 'show_series')
        self._add_menu_entry('A-Z', 'showCharacters')
        self._add_menu_entry('Genre', 'showGenres')
        self._add_menu_entry('Zufall', 'showRandom')
        self._add_menu_entry('Suche', 'showSearch')

    def show_series(self, char=None, specific=None):
        series = self._getJsonContent("series")
        total = len(series)
        cnt = 0
        max = 5

        self._gui.set_view('tvshows')

        for serie in series:
            if cnt == max:
                return
            title = serie["series"].encode('utf-8')

            info_item = VideoInfoItem()
            info_item.tvshowtitle = title

            params = {'id':serie['id'], 'title':title}
            self._add_menu_entry(title, 'show_seasons', info_item=info_item, params=params)
            cnt = cnt + 1

    def show_seasons(self, id, title, specific=None):
        data = self._getJsonContent("series/%s/1" % id)
        rangeStart = not int(data["series"]["movies"])
        total = int(data["series"]["seasons"])

        self._gui.set_view('seasons')

        for i in range(rangeStart, total + 1):
            season_num = str(i)
            if i is 0:
                season_title = 'Film(e)'
                func_name = 'show_cinema_movies'
            else:
                season_title = '%s - Staffel %s' % (title, season_num)
                func_name = 'show_episodes'

            info_item = VideoInfoItem()
            info_item.tvshowtitle = title
            info_item.season = season_num

            params = {'id': id, 'title':title, 'season_num':season_num}
            self._add_menu_entry(season_title, func_name, info_item=info_item, params=params)

    def show_episodes(self, title, id, season_num):
        data = self._getJsonContent("series/%s/%s" % (id, season_num))
        total = len(data['epi'])

        self._gui.set_view('episodes')

        for episode in data['epi']:
            episode_title = "%d - " % int(episode['epi'])
            if episode['german']:
                episode_title += episode['german'].encode('utf-8')
            else:
                episode_title += episode['english'].encode('utf-8')

            info_item = VideoInfoItem()
            info_item.tvshowtitle = title
            info_item.season = season_num
            info_item.episode = episode['epi']

            params = {'id': id, 'title':title, 'season_num': season_num, 'episode_num': episode['epi']}
            self._add_menu_entry(episode_title, 'show_hosters', info_item=info_item, params=params)

    def show_hosters(self, id, season_num, episode_num):
        data = self._getJsonContent("series/%s/%s/%s" % (id, season_num, episode_num))
        if not data:
            return []

        hosters = []
        for link in data['links']:
            hoster = dict()
            hoster['link'] = self.URL_MAIN + 'watch/' + link['id']
            hoster['name'] = link['hoster']
            if hoster['name'] == "OpenLoadHD":
                hoster['name'] = "OpenLoad"
            hoster['displayedName'] = link['hoster']
            hosters.append(hoster)
        if hosters:
            hosters.append('getHosterUrl')
        print hosters

    def _getJsonContent(self, url_part):
        content = self.net.http_GET(self.URL_MAIN + url_part, headers=get_headers(url_part)).content
        json_data = json.loads(content)

        if json_data:
            if 'error' in json_data:
                logger.info("API-Error: %s" % json_data)
                if 'unauthorized' in json_data and json_data['unauthorized'] == 'timestamp':
                    xbmcgui.Dialog().ok('xStream', 'Fehler bei API-Abfrage:', '', 'System-Zeit ist nicht korrekt.')
                else:
                    xbmcgui.Dialog().ok('xStream', 'Fehler bei API-Abfrage:', '', str(json_data))
                return []
            else:
                return json_data
        else:
            return []

    @classmethod
    def custom_settings(cls, settings):
        settings.create_input_text('username', 'Benutzername', enable='!eq(-1,false)')
        settings.create_input_text('password', 'Passwort', option='hidden', enable='!eq(-2,false)')
