# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'mykino_to'
SITE_NAME = 'MyKino'

URL_MAIN = 'http://mykino.to/'
URL_Kinofilme = URL_MAIN + 'aktuelle-kinofilme/'
URL_FILME = URL_MAIN + 'filme/'
URL_SEARCH = URL_MAIN + 'index.php?do=search&subaction=search&story=%s'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_Kinofilme)
    oGui.addFolder(cGuiElement('Aktuelle Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Genre Filme', SITE_IDENTIFIER, 'showGenreFilme'), params)  
    oGui.addFolder(cGuiElement('Genre Serien', SITE_IDENTIFIER, 'showGenreSerie'), params)
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'AZ'), params)    
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors = (sGui is not False)).request()
    parser = cParser()
    pattern = 'caption2"><a[^<]href="([^"]+).*?src="([^"]+).*?">([^<]+).*?<br>Jahr:[^<]([^<]+)'
    
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)

    for sUrl, sThumbnail,  sName, sYear in aResult:
            oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setYear(sYear)
            params.setParam('entryUrl', sUrl)
            oGui.addFolder(oGuiElement, params, False, total)

    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '<a[^>]href="([^"]+)">Weiter</a>')
    if isMatchNextPage:
        params.setParam('sUrl', sNextUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setEndOfDirectory()

def showHosters():
    oParams = ParameterHandler()
    sUrl = oParams.getValue('entryUrl')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    hosters = []
    parser = cParser()
    isMatch, sContainer = parser.parseSingleResult(sHtmlContent, '<ul[^>]class="mirrors-selector".*?<ul class="mirrors-list[^>]loading">')
    if not isMatch:
        return hosters
    isMatch, aResult = parser.parse(sContainer, '://([^/]+)([^#]+)')
    if not isMatch:
        return hosters
    for sName, sUrl in aResult:
            hoster = {}
            hoster['name'] = sName.strip().replace('www.','')
            hoster['link'] = 'http://' + sName + sUrl
            hosters.append(hoster)

    if hosters:
        hosters.append('getHosterUrl')

    return hosters

def getHosterUrl(sUrl=False):
    if not sUrl: sUrl = ParameterHandler().getValue('url')
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

def AZ():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<div[^>]class="catalog-nav">.*?</div>'
    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
       return

    pattern = '<a[^>]href="([^"]+)" >([^<]+)'
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sUrl, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sName , SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()   

def showGenreFilme():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<div[^>]class="contab"[^>]id="tabln1">.*?</li>[^>].*?</ul>'
    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
       return

    pattern = '<a[^>]href="([^"]+).*?">([^<]+)'
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sUrl, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sName , SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()

def showGenreSerie():
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<div[^>]class="contab"[^>]id="tabln2">.*?</li>[^>].*?</ul>'

    isMatch, sContainer = cParser().parseSingleResult(sHtmlContent, pattern)

    if not isMatch:
       return

    pattern = '<a[^>]href="([^"]+).*?">([^<]+)'
    isMatch, aResult = cParser().parse(sContainer, pattern)

    if not isMatch:
        return

    oGui = cGui()
    params = ParameterHandler()
    for sUrl, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sName , SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()
