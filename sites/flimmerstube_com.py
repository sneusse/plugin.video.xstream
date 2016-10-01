# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.config import cConfig
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'flimmerstube_com'
SITE_NAME = 'Flimmerstube'
SITE_ICON = 'flimmerstube.png'
SITE_SETTINGS = '<setting default="flimmerstube.com" enable="!eq(-1,false)" id="flimmerstube-domain" label="' + SITE_NAME + ' domain" type="labelenum" values="flimmerstube.do.am|flimmerstube.com" />'

oConfig = cConfig()
DOMAIN = oConfig.getSetting('flimmerstube-domain')

URL_MAIN = 'http://%s' % DOMAIN
URL_MOVIE = URL_MAIN + '/video/'
URL_SEARCH = URL_MOVIE + 'shv'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIE)
    oGui.addFolder(cGuiElement('Horrorfilme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenresList'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showGenresList():
    oGui = cGui()
    params = ParameterHandler()
    sHtmlContent = cRequestHandler(URL_MOVIE).request()
    aResult = cParser().parse(sHtmlContent, '<a[^>]class=[^>]catName[^>][^>]href="([^"]+)"[^>]>([^"]+)</a>')
    if aResult[0] and aResult[1][0]:
        total = len (aResult[1])
        for sUrl, sName in aResult[1]:
            params.setParam('sUrl', sUrl)
            oGui.addFolder(cGuiElement((sName), SITE_IDENTIFIER, 'showEntries'), params, True, total)
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False, sSearchText = None):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl)
    if sSearchText:
        oRequest.addParameters('query', sSearchText)
        oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()
    pattern = '<div[^>]class="ve-screen"[^>]title="([^"(]+)[^>]([^")]+).*?url[^>]([^")]+).*?<a[^>]href="([^">]+)'
    aResult = cParser().parse(sHtmlContent, pattern)

    if aResult[0] and aResult[1][0]:
        total = len (aResult[1])
        for sName, sJahr, sThumbnail, sUrl in aResult[1]:
            if not sThumbnail.startswith('http'):
                sThumbnail = URL_MAIN + sThumbnail
            oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setYear(sJahr)
            params.setParam('entryUrl', sUrl)
            oGui.addFolder(oGuiElement, params, False, total)

    pattern = 'onclick="spages[^>][^>]([^"]+)[^>][^>];return[^>]false;"><span>&raquo;</span></a></span></td></tr></table>.*?location.href=[^>]([^"]+)[^>][^>]page[^>]'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and aResult[1][0]:
       for sNr, Url in aResult[1]:
        params.setParam('sUrl', Url + sNr)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()

def showHosters():
    oParams = ParameterHandler()
    sUrl = oParams.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = 'src=[^>]"([^"]+)"\s'
    aResult = cParser().parse(sHtmlContent, sPattern)
    hosters = []
    if aResult[1]:
        for sUrl in aResult[1]:
            hoster = {}
            hoster['link'] = sUrl
            hoster['name'] = sUrl
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl = False):
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
    showEntries(URL_SEARCH, oGui, sSearchText)
