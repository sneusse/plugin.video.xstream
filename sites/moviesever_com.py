# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib import logger
import re, base64

SITE_IDENTIFIER = 'moviesever_com'
SITE_NAME = 'MoviesEver Beta'
SITE_ICON = 'moviesever.png'
SITE_GLOBAL_SEARCH = False

URL_MAIN = 'http://moviesever.com/'
URL_FILME = URL_MAIN + 'filme/'
URL_SEARCH = URL_MAIN + '?s=%s'


def load():
    params = ParameterHandler()
    oGui = cGui()
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genres', SITE_IDENTIFIER, 'showGenres'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'), params)
    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    params = ParameterHandler()
    valueType = params.getValue('valueType')
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    sPattern = '<h2>Genres</h2>.*?</li></ul></div>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, sPattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    sPattern = '<a[^>]*href="([^"]+)">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContainer, sPattern)

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

    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False)).request()
    sPattern = 'class="item[^>]*movies">.*?<img[^>]*src="([^"]+)?.*?(?:<span[^>]*class="quality">?([^<]+).*?)?.*?<a[^>]*href="([^"]+)">([^<]+).*?<span>?([^<]+).*?<div[^>]*class="texto">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sThumbnail, sQualy, sUrl, sName, sYear, sDesc in aResult:
        if sThumbnail and not sThumbnail.startswith('http'):
            sThumbnail = URL_MAIN + sThumbnail
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(sThumbnail)
        if sYear:
            oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)
#        params.setParam('sQualy', sQualy)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, False, total)

    if not sGui:
        sPattern = "span[^>]*class=[^>]*current[^>]*>.*?</span><a[^>]*href='([^']+)"
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent, sPattern)
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

        oGui.setView('movies')
        oGui.setEndOfDirectory()


def __decodeHash(sHash):
    sHash = sHash.replace("!BeF", "R")
    sHash = sHash.replace("@jkp", "Ax")
    try:
        sUrl = base64.b64decode(sHash)
        return sUrl
    except:
        logger.error("Invalid Base64: %s" % sHash)


def showHosters():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = '{"link":"(.*?)"}'
    isMatch, aResult = cParser.parse(sHtmlContent, sPattern)

    if not isMatch:
        return []

    hosters = []
    for sUrl in aResult:
        sUrl = __decodeHash(sUrl)
        hname = 'Unknown Hoster'
        try:
            hname = re.compile('^(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n]+)', flags=re.I | re.M).findall(sUrl)[0]
        except:
            pass

        hosters.append({'link': sUrl, 'name': hname})
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
    oGui = cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl).request()
    sPattern = '<div[^>]*class="search-page">.*?<footer[^>]*class="main">'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, sPattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    sPattern = '<img src="([^"]+).*?<div class="title"><a href="([^"]+)">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContainer, sPattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sThumbnail, sUrl, sName in aResult:
        if sThumbnail and not sThumbnail.startswith('http'):
            sThumbnail = URL_MAIN + sThumbnail
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, False, total)


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    if not sSearchText: return
    showSearchEntries(URL_SEARCH % sSearchText.strip(), oGui)
