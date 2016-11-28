# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re, json

SITE_IDENTIFIER = 'rapidstream_to'
SITE_NAME = 'RapidStream'
SITE_ICON = 'rapidstream.png'

URL_MAIN = 'http://rapidstream.to/'
URL_MOVIES = URL_MAIN + 'filme'
URL_SHOWS = URL_MAIN + 'tvshows'
URL_MOSTSEEN = URL_MAIN + 'meistgesehen?get=%s'
URL_SEARCH = URL_MAIN + 'search/%s/'

QUALITY_ENUM = {'240': 0, '360': 1, '480': 2, '720': 3, '1080': 4}


def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showContentMenu'), params)
    #oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showContentMenu():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')

    params.setParam('sUrl', entryUrl)
    oGui.addFolder(cGuiElement('Neu hinzugefügt', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOSTSEEN % ('tv' if 'tvshow' in entryUrl else 'movies'))
    oGui.addFolder(cGuiElement('Meistgesehen', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', entryUrl)
    params.setParam('valueType', 'genre')
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showValueList'), params)
    params.setParam('sUrl', entryUrl)
    params.setParam('valueType', 'year')
    oGui.addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showValueList'), params)
    oGui.setEndOfDirectory()


def showValueList():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    valueType = params.getValue('valueType')
    sHtmlContent = cRequestHandler(entryUrl).request()

    sPattern = '<ul[^>]*class="[^"]*%s[^"]*">(.*?)</ul>' % valueType
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, sPattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    sPattern = '<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
    isMatch, aResult = cParser.parse(sHtmlContainer, sPattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    for sUrl, sName in aResult:
        sName = cUtil.unescape(sName.decode('utf-8')).encode('utf-8')
        params.setParam('sUrl', sUrl)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')

    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False)).request()
    sPattern = '<article[^>]*class="item ([^"]+)"[^>]*>.*?'  # typ
    sPattern += '<a[^>]*href="([^"]+)"[^>]*>\s*<img[^>]*src="([^"]+)"[^>]*>.*?'  # url / thumbnail
    sPattern += '<h3>\s*<a[^>]*>([^<]*)</a>\s*</h3>.*?'  # name
    sPattern += '(?:<span>(\d+)</span>.*?)?'  # url / thumbnail
    sPattern += '</article>'  # container end
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sTyp, sUrl, sThumbnail, sName, sYear in aResult:
        isTvshow = True if sTyp == 'tvshows' else False
        sName = cUtil.unescape(sName.decode('utf-8')).encode('utf-8')
        sThumbnail = re.sub('-\d+x\d+\.', '.', sThumbnail)

        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        oGuiElement.setThumbnail(sThumbnail)
        if sYear:
            oGuiElement.setYear(sYear)
        params.setParam('entryUrl', sUrl)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui:
        sPattern = '<link[^>]*rel="next"[^>]*href="([^"]+)'
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent, sPattern)
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

        oGui.setView('tvshows' if 'tvshows' in entryUrl else 'movies')
        oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    sTVShowTitle = params.getValue('sName')

    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = '<span[^>]*class="se-t[^"]*"[^>]*>(\d+)</span>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sSeasonNr in aResult:
        oGuiElement = cGuiElement("Staffel " + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sSeasonNr', int(sSeasonNr))
        oGui.addFolder(oGuiElement, params, True, total)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sTVShowTitle = params.getValue('TVShowTitle')
    entryUrl = params.getValue('entryUrl')
    sSeasonNr = params.getValue('sSeasonNr')

    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = '<span[^>]*class="se-t[^"]*">%s</span>.*?<ul[^>]*class="episodios"[^>]*>(.*?)</ul>' % sSeasonNr
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    print sSeasonNr
    print sContainer

    pattern = '<li>.*?'
    pattern += '<a[^>]*href="([^"]+)"[^>]*>\s*(?:<img[^>]*src="([^"]+)"[^>]*>)?.*?'  # url / thumbnail
    pattern += '<div[^>]*class="numerando">[^-]*-\s*(\d+)\s*?</div>.*?'  # episodenr
    pattern += '<a[^>]*>([^<]*)</a>.*?'  # name
    pattern += '</li>'
    isMatch, aResult = cParser.parse(sContainer, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sUrl, sThumbnail, sEpisodeNr, sName in aResult:
        sName = cUtil.unescape(sName.decode('utf-8')).encode('utf-8')
        sThumbnail = re.sub('-\d+x\d+\.', '.', sThumbnail)

        oGuiElement = cGuiElement("%s - %s" % (sEpisodeNr, sName.strip()), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setEpisode(sEpisodeNr)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('episode')
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, False, total)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showHosters():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()

    sPattern = '<iframe[^>]*class="metaframe"[^>]*src="([^"]+)"[^>]*>'  # url
    isMatch, streamUrl = cParser.parseSingleResult(sHtmlContent, sPattern)

    if not isMatch:
        return []

    sHtmlContent = cRequestHandler(streamUrl).request()
    isMatch, sJson = cParser.parseSingleResult(sHtmlContent, '(\[{".*?}\])')

    if not isMatch:
        logger.info("hoster pattern did not match")
        return []

    hosters = []
    for entry in json.loads(sJson):
        if 'file' not in entry or 'label' not in entry: continue
        sLabel = entry['label'].encode('utf-8')
        hoster = dict()
        hoster['link'] = entry['file']
        if entry['label'].encode('utf-8')[:-1] in QUALITY_ENUM:
            hoster['quality'] = QUALITY_ENUM[entry['label'].encode('utf-8')[:-1]]
        hoster['name'] = sLabel
        hosters.append(hoster)

    if hosters:
        hosters.append('playStream')
    return hosters


def playStream(sUrl=False):
    oParams = ParameterHandler()
    if not sUrl: sUrl = oParams.getValue('url')
    return [{'streamUrl': sUrl, 'resolved': True}]


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
