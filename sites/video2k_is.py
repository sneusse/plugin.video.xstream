# -*- coding: utf-8 -*-

import json
import threading
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
    pattern = '<li[^>]*title="(.*?)\((:?\d+)?\).*?(:?\s+-\s+(:?[^"]+))?"[^>]*>.*?' # name / year / desc
    pattern += "<a[^>]*href='([^']*)'[^>]*>.*?" # url
    pattern += "<img[^>]*src='([^']*)'[^>]*>.*?" # img
    pattern += "</li>" # title
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)
    for sName, sYear, sUglyDesc, sDesc, sUrl, sThumbnail in aResult:
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)
        oGui.addFolder(oGuiElement, params, False, total)

    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '</strong>.*?<a[^>]*href="([^"]+)"[^>]*>\d+')
    if isMatchNextPage:
        params.setParam('sUrl', cUtil().unescape(sNextUrl))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setEndOfDirectory()

def getHosters(sUrl = False):
    return []

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
