# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
import json

SITE_IDENTIFIER = 'movietown_org'
SITE_NAME = 'Movietown'
SITE_ICON = 'movietown.png'

URL_MAIN = 'http://movietown.org/'
URL_LIST = URL_MAIN + 'titles/paginate?_token=%s&perPage=%s&page=%s&order=%s&type=%s'


def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    params = ParameterHandler()
    params.setParam('order', 'release_dateDesc')
    params.setParam('type', 'movie')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('order', 'release_dateDesc')
    params.setParam('type', 'series')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    order = params.getValue('order')
    type = params.getValue('type')

    hasToken, token = __getToken()

    if not hasToken:
        if not sGui: oGui.showError('xStream', 'Es wurde kein Token gefunden.')
        return

    iPage = int(params.getValue('page'))
    if iPage <= 0:
        iPage = 1

    sUrl = URL_LIST % (token, 25, iPage, order, type)
    sJson = cRequestHandler(sUrl, ignoreErrors=True).request()

    if not sJson:
        if not sGui: oGui.showError('xStream', 'Fehler beim Laden der Daten.')
        return

    aJson = json.loads(sJson)

    if not 'items' in aJson or len(aJson['items']) == 0:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aJson['items'])
    for item in aJson["items"]:
        isTvshow = True if item['type'] == 'series' else False
        oGuiElement = cGuiElement(item['title'].encode('utf-8'), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        oGuiElement.setThumbnail(item['poster'])
        oGuiElement.setYear(item['year'])
        oGuiElement.setDescription(item['plot'])
        if item['runtime']:
            oGuiElement.addItemValue('duration', int(item['runtime']) * 60)
        if isTvshow:
            oGuiElement.setFunction('showSeasons')
            oGuiElement.setTVShowTitle(item['title'].encode('utf-8'))
        params.setParam('title_id', item['id'])
        params.setParam('sUrl', sUrl)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if float(aJson["totalPages"]) > iPage:
        params.setParam('page', (iPage + 1))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    oGui.setView('movies')
    oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    oParams = ParameterHandler()
    title_id = oParams.getValue('title_id')
    sUrl = oParams.getValue('sUrl')
    sJson = cRequestHandler(sUrl).request()

    if not sJson:
        oGui.showError('xStream', 'Fehler beim Laden der Daten.')

    aJson = json.loads(sJson)

    if not 'items' in aJson or len(aJson['items']) == 0:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    tvshowItem = False

    aSeasons = []
    for item in aJson['items']:
        if item['id'] != title_id:
            continue
        tvshowItem = item
        for link in item['link']:
            isseason = int(link['season'])

            if isseason not in aSeasons:
                aSeasons.append(isseason)

    total = len(aJson['items'])
    for season in sorted(aSeasons):
        oGuiElement = cGuiElement('Staffel ' + str(season), SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(tvshowItem['title'].encode('utf-8'))
        oGuiElement.setThumbnail(tvshowItem['poster'])
        oGuiElement.setYear(tvshowItem['year'])
        oGuiElement.setDescription(tvshowItem['plot'])
        if tvshowItem['runtime']:
            oGuiElement.addItemValue('duration', int(tvshowItem['runtime']) * 60)
        oGuiElement.setSeason(season)
        oGui.addFolder(oGuiElement, oParams, True, total)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    oParams = ParameterHandler()
    title_id = oParams.getValue('title_id')
    sSeason = oParams.getValue('season')
    sUrl = oParams.getValue('sUrl')
    sJson = cRequestHandler(sUrl).request()

    if not sJson:
        oGui.showError('xStream', 'Fehler beim Laden der Daten.')

    aJson = json.loads(sJson)

    if not 'items' in aJson or len(aJson['items']) == 0:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    tvshowItem = False

    aEpisodes = []
    for item in aJson['items']:
        if item['id'] != title_id:
            continue
        tvshowItem = item
        for link in item['link']:
            if link['season'] != sSeason:
                continue

            iepisode = int(link['episode'])

            if iepisode not in aEpisodes:
                aEpisodes.append(iepisode)

    total = len(aJson['items'])
    for episode in sorted(aEpisodes):
        oGuiElement = cGuiElement('Folge ' + str(episode), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('episode')
        oGuiElement.setTVShowTitle(tvshowItem['title'].encode('utf-8'))
        oGuiElement.setThumbnail(tvshowItem['poster'])
        oGuiElement.setYear(tvshowItem['year'])
        oGuiElement.setDescription(tvshowItem['plot'])
        if tvshowItem['runtime']:
            oGuiElement.addItemValue('duration', int(tvshowItem['runtime']) * 60)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(episode)
        oGui.addFolder(oGuiElement, oParams, False, total)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def showHosters():
    oParams = ParameterHandler()
    title_id = oParams.getValue('title_id')
    sUrl = oParams.getValue('sUrl')
    sSeason = oParams.getValue('season')
    sEpisode = oParams.getValue('episode')
    sJson = cRequestHandler(sUrl).request()
    hosters = []

    if not sJson:
        return hosters

    print sSeason
    print sEpisode

    aJson = json.loads(sJson)
    for item in aJson['items']:
        if item['id'] != title_id:
            continue
        for link in item['link']:
            if sSeason and sEpisode:
                if link['season'] != sSeason: continue
                if link['episode'] != sEpisode: continue

            hoster = dict()
            hoster['link'] = link["url"]
            hoster['name'] = link["label"].encode('utf-8').Title()
            hosters.append(hoster)

    if hosters:
        hosters.append('play')
    return hosters


def play(sUrl=False):
    oParams = ParameterHandler()
    if not sUrl: sUrl = oParams.getValue('url')
    return [{'streamUrl': sUrl, 'resolved': False}]


def __getToken():
    sHtmlContent = cRequestHandler(URL_MAIN, ignoreErrors=True).request()
    return cParser.parseSingleResult(sHtmlContent, "token\s*:\s*'([\w|\d]+)'")
