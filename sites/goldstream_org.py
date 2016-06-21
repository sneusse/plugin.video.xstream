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

SITE_IDENTIFIER = 'goldstream_org'
SITE_NAME = 'Goldstream'
SITE_ICON = 'goldstream_org.png'

URL_MAIN = 'http://goldstream.org/'
URL_Kinofilme = URL_MAIN + 'Stream/kinofilme/'
URL_Filme = URL_MAIN + 'Stream/filme/'
URL_SEARCH =  URL_MAIN + '?s=%s'

URL_GENRES_LIST = {'Abenteuer' : 'Stream/filme/abenteuer', 'Action' : 'Stream/filme/action', 'Animation' : 'Stream/filme/animation', 'Dokumentation' : 'Stream/filme/dokumentation',
                  'Drama' : 'Stream/filme/drama',  'Family' : 'Stream/filme/family',  'Historie' : 'Stream/filme/historie',  'Horror' : 'Stream/filme/horror',
                  'Kom�die' : 'Stream/filme/komoedie',  'Krimi' : 'Stream/filme/krimi',  'Lovestory' : 'Stream/filme/lovestory',  'Musical' : 'Stream/filme/musical', 
				  'Science Fiction' : 'Stream/filme/science-fiction', 'Thriller' : 'Stream/filme/thriller', 'Western' : 'Stream/filme/western', 'Erotik' : 'Stream/filme/erotik'}

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
  
    params.setParam('sUrl', URL_Kinofilme)
    oGui.addFolder(cGuiElement('Kino Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_Filme)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenresList'), params)
    params.setParam('sUrl', URL_SEARCH)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showGenresList():
    oGui = cGui()
    for key in sorted(URL_GENRES_LIST):
        params = ParameterHandler()
        params.setParam('sUrl', (URL_MAIN + URL_GENRES_LIST[key]))
        oGui.addFolder(cGuiElement(key, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl).request()

    pattern ='class="entry-title"><a href="([^"]+).*?.*?title="Direkter Link zu([^"]+)">.*?<p><p>([^"[]+)'

    aResult = cParser().parse(sHtmlContent, pattern)

    if len(aResult) > 0:

        for result in aResult[1]:
            oGuiElement = cGuiElement(result[1].replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '\'').replace('&#8220;', '"').replace('&#8222;', '"'), SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setDescription(result[2].replace('&#8220;', '"').replace('&#8222;', '"').replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '\''))
            params.setParam('entryUrl', result[0])
            params.setParam('sName', result[1])
            oGui.addFolder(oGuiElement, params, bIsFolder = False,)
            oGui.setView('movies')
   #check next page
	pattern = '<div class="right"><a href="([^"]+)">'
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

    sPattern = '<a title=".*?Stream .*?" href="([^"]+).*?blank">([^"]+) </a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern,)
    hosters = []                                     # hosterliste initialisieren
    sFunction='getHosterUrl'                         # folgeFunktion festlegen 
    if aResult[1]:
        for aEntry, name in aResult[1]:
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