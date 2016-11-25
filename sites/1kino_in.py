# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = '1kino_in'
SITE_NAME = '1Kino'
SITE_ICON = '1kino.png'

URL_MAIN = 'http://1kino.in/'
URL_KINO = URL_MAIN + 'kinofilme'
URL_FILME = URL_MAIN + 'filme'
URL_SHOWS = URL_MAIN + 'serien'
URL_SEARCH = URL_MAIN + '?s=%s'
URL_EPISODE = URL_MAIN + 'drop.php'


def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_KINO)
    oGui.addFolder(cGuiElement('Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'))
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    parser = cParser()
    isMatch, sHtmlContainer = parser.parseSingleResult(sHtmlContent, 'Filme</a><ul[^>]class="sub-menu">.*?</a></li></ul>')

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    isMatch, aResult = parser.parse(sHtmlContainer, 'href="([^"]+)">([^<]+)')

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    for sUrl, sName in aResult:
        params.setParam('sUrl', sUrl)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')

    oRequestHandler = cRequestHandler(entryUrl)
    sHtmlContent = oRequestHandler.request()

    parser = cParser()
    pattern = '"><a[^>]*href="([^"]+)"[^>]*rel="([^"]+).*?title="([^"(]+)[^>]([^)]+).*?<div[^>]*class="ui-des">([^"<]+)'
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sUrl, sThumbnail, sName, sYear, sDesc in aResult:
        isTvshow = True if "serien" in entryUrl else False
        if (URL_SEARCH % '') in entryUrl:
            sHtmlContent = cRequestHandler(sUrl, ignoreErrors=(sGui is not False)).request()
            isTvshow, aDummyResult = cParser.parse(sHtmlContent, '<option value="([^"]+)">([^ ]+)([^<]+)')

        oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER, 'showHosters')
        sThumbnail = re.sub('-\d+x\d+\.', '.', sThumbnail)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setYear(sYear)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', sUrl)
        params.setParam('isTvshow', isTvshow)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sDesc', sDesc)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui:
        isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, "<a[^>]*class=\"nextpostslink\"[^>]*rel=\"next\"[^>]*href=\"([^\"]+)")
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

        oGui.setView('tvshows' if 'serien' in entryUrl else 'movies')
        oGui.setEndOfDirectory()


def showHosters():
    params = ParameterHandler()
    isTvshowEntry = params.getValue('isTvshow')

    if isTvshowEntry == 'True':
        entryUrl = params.getValue('entryUrl')
        sHtmlContent = cRequestHandler(entryUrl).request()
        pattern = '<option value="([^"]+)">([^ ]+)([^<]+)'
        pattern2 = 'postID="([^"]+)"'
        isMatch, aResult = cParser().parse(sHtmlContent, pattern)
        isMatch, aResult2 = cParser().parse(sHtmlContent, pattern2)
        for postID in aResult2:
            params.setParam('postID', postID)

        if isMatch:
            showSeason(aResult, params)
    else:
        return getHosters()


def showSeason(aResult, params):
    oGui = cGui()
    sThumbnail = params.getValue('sThumbnail')
    sTVShowTitle = params.getValue('sName')
    sDesc = params.getValue('sDesc')

    total = len(aResult)
    for sId, sSeason, sSeasonNr in aResult:
        oGuiElement = cGuiElement(sSeason + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sSeasonNr', sSeasonNr)
        params.setParam('sId', sId)
        oGui.addFolder(oGuiElement, params, True, total)

    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sThumbnail = params.getValue('sThumbnail')
    sSeasonNr = params.getValue('sSeasonNr')
    sId = params.getValue('sId')
    postID = params.getValue('postID')
    sTVShowTitle = params.getValue('TVShowTitle')
    sDesc = params.getValue('sDesc')

    oRequest = cRequestHandler(URL_EPISODE)
    oRequest.addParameters('ceck', 'sec')
    oRequest.addParameters('option', sId)
    oRequest.addParameters('pid', postID)

    oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()
    parser = cParser()
    pattern = '<option value="([^"]+)">([^ ]+)([^<]+)'

    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        return

    total = len(aResult)

    for shID, sName, Episodenr in aResult:
        oGuiElement = cGuiElement(sName + Episodenr, SITE_IDENTIFIER, 'getHosters')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setEpisode(Episodenr)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setMediaType('episode')
        params.setParam('shID', shID)
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def getHosters():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    isTvshowEntry = params.getValue('isTvshow')
    shID = params.getValue('shID')
    postID = params.getValue('postID')
    if isTvshowEntry == 'True':
        oRequest = cRequestHandler(URL_EPISODE)
        oRequest.addParameters('ceck', 'sec')
        oRequest.addParameters('option', shID)
        oRequest.addParameters('pid', postID)
        oRequest.setRequestType(1)
        sHtmlContent = oRequest.request()
    else:
        sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = '<div[^>]id="stream-links"><a[^>]target="_blank"[^>]rel="nofollow"[^>]href="([^"]+).*?blank">([^<]+)'
    aResult = cParser().parse(sHtmlContent, sPattern)
    hosters = []
    if aResult[1]:
        for sUrl, sName in aResult[1]:
            hoster = {'link': sUrl, 'name': sName}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    if not sUrl: sUrl = ParameterHandler().getValue('sUrl')
    refUrl = ParameterHandler().getValue('entryUrl')
    oRequest = cRequestHandler(sUrl, caching=False)
    oRequest.addHeaderEntry("Referer", refUrl)
    oRequest.request()
    sUrl = oRequest.getRealUrl()

    return {'streamUrl': sUrl, 'resolved': False}


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
