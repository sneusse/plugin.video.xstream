# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'video2k_is'
SITE_NAME = 'Video2k'
SITE_ICON = 'Video2k.png'

URL_MAIN = 'http://www.video2k.is/'
URL_MOVIE = URL_MAIN + '?c=movie&m=%s'
URL_SEARCH = URL_MAIN + '?keyword=%s&c=movie&m=filter'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl',URL_MOVIE % 'releases')
    oGui.addFolder(cGuiElement('Neu', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'featured')
    oGui.addFolder(cGuiElement('Kino', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'views')
    oGui.addFolder(cGuiElement('Top', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_MOVIE % 'updates')
    oGui.addFolder(cGuiElement('Updates', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')

    oRequestHandler = cRequestHandler(entryUrl)
    sHtmlContent = oRequestHandler.request()

    parser = cParser()
    pattern ='<li[^>]title="([^">]+).*?([^-/d]+)-film[^>]stream[^>]([^.]+).*?<img[^>]src=[^>]([^?<]+)[^>][^>]border.*?<a[^>]href=.*?>([^<]+)'
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)
    for sDescription, sYear, sUrl, sThumbnail, sName in aResult:
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setDescription(cUtil().unescape(sDescription.decode('utf-8')).encode('utf-8'))
            oGuiElement.setYear(sYear)
            params.setParam('entryUrl', 'http://video2k.is/?c=ajax&m=movieStreams2&id=' + sUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            oGui.addFolder(oGuiElement, params, bIsFolder = False,)
    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '</strong>.*?<a[^>]*href="([^"]+)"[^>]*>\d+')
    if isMatchNextPage:
        params.setParam('sUrl', cUtil().unescape(sNextUrl))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    if not sGui:
        oGui.setEndOfDirectory()

def showHosters():
    oParams = ParameterHandler()
    sUrl = oParams.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = 'show[^>]player.*?, "([^"]+)".*?domain=([^">]+)[^>]'
    aResult = cParser().parse(sHtmlContent, sPattern)
    hosters = []
    if aResult[1]:
        for sUrl, sName in aResult[1]:
            hoster = {}
            hoster['link'] = sUrl
            hoster['name'] = sName
            hosters.append(hoster)         
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl = False):
    oParams = ParameterHandler()
    if not sUrl: sUrl = oParams.getValue('url')
    logger.info("url %s" % sUrl)
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
