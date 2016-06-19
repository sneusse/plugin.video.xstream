# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'cine-dream_net'
SITE_NAME = 'CineDream'
SITE_ICON = 'cine-dream_net.png'

URL_MAIN = 'Http://www.cine-dream.net/'
URL_SEARCH =  URL_MAIN + '?s=%s'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Kategorien', SITE_IDENTIFIER, 'showKategorie'), params)
    params.setParam('sUrl', URL_SEARCH)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()
	
def showKategorie():
    params = ParameterHandler()
    oGui = cGui()
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = 'class="cat-item.*?a[^>]*href="([^"]+)" title="([^"]+)' # url / title
    aResult = cParser().parse(sHtmlContent, pattern)

    for sUrl, sTitle in aResult[1]:
        params.setParam('sUrl', sUrl)
        oGui.addFolder(cGuiElement(sTitle.strip(), SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()
	
def showEntries(entryUrl = False, sGui = False):
    oGui = cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern ='<div class="thumbnail">.*? <a href="([^"]+)" title="([^"]+)">.*?<img src="([^"]+)'
    aResult = cParser().parse(sHtmlContent, pattern)

    if len(aResult) > 0:

        for result in aResult[1]:
            oGuiElement = cGuiElement(result[1].replace('&#8220;', '"').replace('&#8222;', '"').replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '\''), SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setThumbnail(result[2])
            params.setParam('entryUrl', result[0])
            params.setParam('sName', result[1])
            params.setParam('sThumbnail', result[2])
            oGui.addFolder(oGuiElement, params, bIsFolder = False,)
            oGui.setView('movies')
            
    #check next page
	pattern = '<a class="nextpostslink".*? href="([^"]+)'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and aResult[1][0]:
        params.setParam('sUrl', aResult[1][0])
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    if not sGui:
        oGui.setEndOfDirectory()
        return

def showHosters():
    oParams = ParameterHandler() #Parameter laden
    sUrl = oParams.getValue('entryUrl')  # Weitergegebenen Urlteil aus den Parametern holen 
    oRequestHandler = cRequestHandler(sUrl) # gesamte Url zusammesetzen
    sHtmlContent = oRequestHandler.request()         # Seite abrufen
    sPattern = '>Stream:.*?([^" ]+).*?<center><a href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern,)
    hosters = []                                     # hosterliste initialisieren
    sFunction='getHosterUrl'                         # folgeFunktion festlegen 
    if aResult[1]:
        for name, aEntry in aResult[1]:
            hoster = {} 
            hoster['link'] = aEntry
            # extract domain name
            hoster['name'] = name
            hosters.append(hoster)
        hosters.append(sFunction)
    return hosters

def getHosterUrl(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()
    # URL ermitteln falls nicht �bergeben
    if not sUrl: sUrl = oParams.getValue('url')
    logger.info("url %s" % sUrl)
    # Array mit einem Eintrag f�r Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results
    # Ergebniss zur�ckliefern
	
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setView('movies')
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)