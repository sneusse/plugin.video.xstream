# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler

SITE_IDENTIFIER = 'de_ddl_me'
SITE_NAME = 'de.ddl.me'
SITE_ICON = 'ddl.png'

URL_MAIN = 'http://de.ddl.me'

def load():
    oGui = cGui()
   
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()
   
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False and sSearchText != ''):
        _search(oGui, sSearchText)
    else:
        return
    oGui.setEndOfDirectory()
    
def _search(oGui, sSearchString):
    searchUrl = URL_MAIN + '/search_99/?q='
    
    oRequest = cRequestHandler(searchUrl + sSearchString)
    content = oRequest.request()
    searchPattern = "class='iwrap type_0'.*?title='([^']+)' href='([^']+)'.*?<img alt='.*?' src='([^']+)'>"
    oParser = cParser()
    aResult = oParser.parse(content, searchPattern)
    if not aResult[0]:
        return
    ###### parse entries
    params = ParameterHandler()
    function = 'getHosters'
    iTotal = len(aResult[1])
    for title, link, img in aResult[1]:
        sLabel = title
        sTitle = sLabel
        sNextUrl = link
        params.setParam('siteUrl',sNextUrl)
        oGuiElement = cGuiElement(sTitle, SITE_IDENTIFIER, function)
        oGuiElement.setThumbnail(img)
        oGuiElement.setMediaType('movie')
        oGui.addFolder(oGuiElement, params, bIsFolder = False, iTotal = iTotal)
            
def getHosters():
    oParams = ParameterHandler() #Parameter laden
    sUrl = oParams.getValue('siteUrl')  # Weitergegebenen Urlteil aus den Parametern holen
   
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl) # gesamte Url zusammesetzen
    sHtmlContent = oRequestHandler.request()         # Seite abrufen

    sHtmlContent = sHtmlContent.replace('\\','')
    sPattern = '"\d{1,2}","\w+",".*?","([^"]+)","\d+","stream"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern, ignoreCase = True)
    hosters = []                                     # hosterliste initialisieren
    sFunction='getHosterUrl'                         # folgeFunktion festlegen
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            hoster = {}
            hoster['link'] = aEntry
            # extract domain name
            temp = aEntry.split('//')
            temp = str(temp[-1]).split('/')
            temp = str(temp[0]).split('.')
            hoster['name'] = temp[-2]
            hosters.append(hoster)
        if len(hosters) > 0:
            hosters.append(sFunction)
    return hosters
   
def getHosterUrl(sStreamUrl = False):
    if not sStreamUrl:
        params = ParameterHandler()
        sStreamUrl = params.getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sStreamUrl
    result['resolved'] = False
    results.append(result)
    return results