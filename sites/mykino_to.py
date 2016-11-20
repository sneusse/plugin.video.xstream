# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
# import json

SITE_IDENTIFIER = 'mykino_to'
SITE_NAME = 'MyKino'
SITE_ICON = 'mykino.png'

URL_MAIN = 'http://mykino.to/'
URL_Kinofilme = URL_MAIN + 'aktuelle-kinofilme/'
URL_FILME = URL_MAIN + 'filme/'
URL_SERIE = URL_MAIN + 'serien/'
URL_SEARCH = URL_MAIN + 'index.php?do=search&subaction=search&story=%s'
URL_EPISODE = URL_MAIN + 'engine/ajax/a.sseries.php'


def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_Kinofilme)
    oGui.addFolder(cGuiElement('Aktuelle Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIE)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    params.setParam('sGenreId', 1)
    oGui.addFolder(cGuiElement('Genre Filme', SITE_IDENTIFIER, 'showGenre'), params)
    params.setParam('sUrl', URL_MAIN)
    params.setParam('sGenreId', 2)
    oGui.addFolder(cGuiElement('Genre Serien', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showAlphaNumeric'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showAlphaNumeric():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<div[^>]*class="catalog-nav"[^>]*>(.*?)</div>'
    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
        return

    pattern = '<a[^>]*href="([^"]+)"[^>]*>(\w)</a>'
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sUrl, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showGenre():
    oParams = ParameterHandler()
    sUrl = oParams.getValue('sUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '<div[^>]*id="tabln%s"[^>]*>(.*?)</ul>' % oParams.getValue('sGenreId')
    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
        return

    pattern = '<a[^>]*href="([^"]+)"[^>]*>([^<]*)</a>'
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    for sUrl, sName in aResult:
        oParams.setParam('sUrl', URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), oParams)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False)).request()
    parser = cParser()
    pattern = '"><a[^<]href="([^"]+)/([^-]+)([^"]+).*?src="([^"]+).*?">([^<]+).*?<br>Jahr:[^<]([^<]+)<br>Genre: ([^<]+)'

    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)

    for sDummy, news_id, sUrl, sThumbnail, sName, sYear, sGenre in aResult:
        isTvshow = True if "Serie" in sGenre else False
        oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER,
                                  'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setYear(sYear)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', URL_MAIN + news_id + sUrl)
        params.setParam('isTvshow', isTvshow)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('TVShowTitle', sName)
        params.setParam('sGenre', sGenre)
        params.setParam('news_id', news_id)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui:
        isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '<a[^>]*href="([^"]+)"[^>]*>Weiter</a>')
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        sGenre = params.getValue('sGenre')
        oGui.setView('tvshows' if 'Serie' in sGenre else 'movies')
        oGui.setEndOfDirectory()


def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    isTvshowEntry = params.getValue('isTvshow')

    if isTvshowEntry == 'True':
        sHtmlContent = cRequestHandler(entryUrl).request()
        pattern = '<select[^>]*id="sseriesSeason">.*?</select>'
        isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)
        if not isMatch:
            return
        pattern = '<option value="([^"]+)">([^<]+)'
        isMatch, aResult = cParser().parse(sContainer, pattern)
        if isMatch:
            showSeason(aResult, params)
    else:
        return getHosters()


def showSeason(aResult, params):
    oGui = cGui()
    sThumbnail = params.getValue('sThumbnail')

    total = len(aResult)
    for sId, sSeason in aResult:
        oGuiElement = cGuiElement(sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setSeason(sId)
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sSeason', sId)
        oGui.addFolder(oGuiElement, params, True, total)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sThumbnail = params.getValue('sThumbnail')
    sSeason = params.getValue('sSeason')
    news_id = params.getValue('news_id')
    sTVShowTitle = params.getValue('TVShowTitle')
    oRequest = cRequestHandler(URL_EPISODE)
    oRequest.addParameters('news_id', news_id)
    oRequest.addParameters('season', sSeason)

    oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()
    parser = cParser()
    pattern = '<option value=[^>]"([^"]+)[^>]">([^ ]+)([^<]+)'

    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        return

    total = len(aResult)

    for series, sName, Episodenr in aResult:
        oGuiElement = cGuiElement(sName + Episodenr, SITE_IDENTIFIER,
                                  'getSerienHosters')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(Episodenr)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('episode')
        params.setParam('series', series)
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def getSerienHosters():
    params = ParameterHandler()
    series = params.getValue('series')
    news_id = params.getValue('news_id')

    oRequest = cRequestHandler(URL_EPISODE)
    oRequest.addParameters('news_id', news_id)
    oRequest.addParameters('series', series)
    oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()

    isMatch, aResult = cParser().parse(sHtmlContent, 'data-href=[^"]"([^"]+).*?<span>([^<]+)')
    if not isMatch:
        return []

    hosters = []
    for sUrl, sName in aResult:
        for idx, sLink in enumerate(sUrl.split('#,')):
            hoster = {'name': sName, 'link': sLink.replace('\/', '/'),
                      'displayedName': '%s - Mirror %s' % (sName, idx + 1)}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosters():
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()

    isMatch, aResult = cParser().parse(sHtmlContent, '<a[^>]*data-href="([^"]+)"[^>]*>.*?<span>([^<]*)<\/span>')
    if not isMatch:
        return []

    hosters = []
    for sUrls, sName in aResult:
        for idx, sLink in enumerate(sUrls.split(',')):
            hoster = {'name': sName, 'link': sLink, 'displayedName': '%s - Mirror %s' % (sName, idx + 1)}
            hosters.append(hoster)

    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    if not sUrl: sUrl = ParameterHandler().getValue('url')
    results = []
    result = {'streamUrl': sUrl, 'resolved': False}
    results.append(result)
    return results


def showSearchEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False)).request()
    parser = cParser()
    pattern = 'caption2"><a[^<]href="([^"]+)/([^-]+)([^"]+).*?src="([^"]+).*?">([^<]+).*?Jahr: ([^<]+)'

    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)

    for sDummy, news_id, sUrl, sThumbnail, sName, sYear in aResult:
        sHtmlContent = cRequestHandler(URL_MAIN + news_id + sUrl, ignoreErrors=(sGui is not False)).request()
        parser = cParser()
        pattern = '<select[^>]*id="sseriesSeason">.*?</select>'

        isTvshow, aResult = parser.parse(sHtmlContent, pattern)

        oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER,
                                  'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setYear(sYear)
        params.setParam('entryUrl', URL_MAIN + news_id + sUrl)
        params.setParam('isTvshow', isTvshow)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('TVShowTitle', sName)
        params.setParam('news_id', news_id)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    if not sSearchText: return
    showSearchEntries(URL_SEARCH % sSearchText.strip(), oGui)
