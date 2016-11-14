# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamdream_ws'
SITE_NAME = 'streamdream'
SITE_ICON = 'mykstreamdream.png'

URL_MAIN = 'http://streamdream.ws/'
URL_FILME = URL_MAIN + 'neuefilme'
URL_SERIE = URL_MAIN + 'neueserien'

EPISODE_URL = URL_MAIN + 'episodeholen.php'
URL_HOSTER_URL = URL_MAIN + 'episodeholen2.php'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIE)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)    
    
    params.setParam('sUrl', URL_MAIN)
    params.setParam('valueType', 'film')
    oGui.addFolder(cGuiElement('Genre Filme', SITE_IDENTIFIER, 'showGenre'), params)
    params.setParam('sUrl', URL_MAIN)
    params.setParam('valueType', 'serien')
    oGui.addFolder(cGuiElement('Genre Serien', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.setEndOfDirectory()

    
def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    valueType = params.getValue('valueType')

    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = 'href="%s([^"]+)">([^<]+)</a></li>' % valueType
    aResult = cParser().parse(sHtmlContent, pattern)

    if not aResult[0]:
        return

    for sID, sName in aResult[1]:
        params.setParam('sUrl',entryUrl + valueType + sID)
        oGui.addFolder(cGuiElement(sName , SITE_IDENTIFIER, 'showEntries'), params)  
    oGui.setEndOfDirectory()
    
def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    
    oRequestHandler = cRequestHandler(entryUrl, ignoreErrors = (sGui is not False))
    
    sHtmlContent = oRequestHandler.request()
    parser = cParser()
    pattern = '<a[^>]*class="linkto"[^>]*href="([^"]+)">*[^>]*.*?<img[^>]*src="([^"]+)">([^<]+)'
    
    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)

    for sUrl, sThumbnail, sName in aResult:
        isTvshow = True if 'serie' in sUrl else False
        oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType("tvshow" if 'serie' in sUrl else "movie")
        params.setParam('entryUrl', URL_MAIN + sUrl)
        params.setParam('Name', sName)
        params.setParam('isTvshow', isTvshow)
        params.setParam('sThumbnail', sThumbnail)        
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '<a*[^>]class="righter"*[^>]href="([^"]+)')
    if isMatchNextPage:
        params.setParam('sUrl', entryUrl + sNextUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setView('tvshows' if 'serie' in entryUrl else 'movies')
        oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    isTvshowEntry = params.getValue('isTvshow')

    if isTvshowEntry == 'True':
        oRequest = cRequestHandler(entryUrl)
        oRequest.addHeaderEntry("X-Requested-With","XMLHttpRequest")
        sHtmlContent = oRequest.request()
        
        isMatch, aResult = cParser.parse(sHtmlContent, 'season="([^"]+)[^>]>([^<]+)</div>.*?[^>]*<script>[^>].*?imdbid[^>][^>]"([^"]+).*?language[^>][^>]"([^"]+)"')
        if isMatch:
            showSeason(aResult, params)
    else:
        return getHosters(entryUrl)

        
def showSeason(aResult, params):
    oGui = cGui()

    sTVShowTitle = params.getValue('Name')
    sThumbnail = params.getValue('sThumbnail')
    entryUrl = params.getValue('entryUrl')
    total = len (aResult)
    for sID, sSeasonName , imdbid, slanguage in aResult:
        oGuiElement = cGuiElement(sSeasonName, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setDescription(slanguage)        
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        params.setParam('Season', sID)
        params.setParam('imdbid', imdbid)
        params.setParam('language', slanguage)
    
        
        oGui.addFolder(oGuiElement, params, True, total)


    oGui.setView('seasons')
    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    imdbid = params.getValue('imdbid')
    slanguage = params.getValue('language')
    sSeason = params.getValue('Season')
    sTVShowTitle = params.getValue('Name')
    
    oRequest = cRequestHandler(EPISODE_URL)
    oRequest.addHeaderEntry("X-Requested-With","XMLHttpRequest")
    oRequest.setRequestType(1)
    oRequest.addParameters('imdbid', imdbid)
    oRequest.addParameters('language', slanguage)
    oRequest.addParameters('season', sSeason)
 
    
    sHtmlContent = oRequest.request()
     
    
    isMatch, aResult = cParser.parse(sHtmlContent, '>#([^<]+)</p>[^>]*[^>]*<script>.*?imdbid:[^>]"([^"]+).*?language:[^>]"([^"]+).*?season:[^>]"([^"]+)')
    if isMatch:
       total = len (aResult)
       for sEpisode , imdbid, slanguage, sSeason in aResult:
        oGuiElement = cGuiElement('Folge ' + sEpisode, SITE_IDENTIFIER, 'getserieHosters')
        oGuiElement.setMediaType('season')
        oGuiElement.setSeason(sSeason)        
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        params.setParam('Episode', sEpisode)
        params.setParam('Season', sSeason)
        params.setParam('imdbid', imdbid)
        params.setParam('language', slanguage)
    
        
        oGui.addFolder(oGuiElement, params, False, total)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def getserieHosters():
    oGui = cGui()
    params = ParameterHandler()
    sThumbnail = params.getValue('sThumbnail')
    imdbid = params.getValue('imdbid')
    slanguage = params.getValue('language')
    sSeason = params.getValue('Season')
    sEpisode = params.getValue('Episode')
    
    oRequest = cRequestHandler(URL_HOSTER_URL)
    oRequest.addHeaderEntry("X-Requested-With","XMLHttpRequest")
    oRequest.setRequestType(1)
    oRequest.addParameters('imdbid', imdbid)
    oRequest.addParameters('language', slanguage)
    oRequest.addParameters('season', sSeason)
    oRequest.addParameters('episode', sEpisode)
    
    sHtmlContent = oRequest.request()
     
    
    isMatch, aResult = cParser.parse(sHtmlContent, '<a href="([^"]+)//([^"/]+)([^"]+)" target="_blank"><img class="sd')
    hosters = []
    if isMatch:
   
        for sHttp, sName, sUrl in aResult:
            hoster = {}
            hoster['link'] = sHttp + '//' + sName + sUrl
            hoster['name'] = sName
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters       

def getHosters(sUrl=False):
    oParams = ParameterHandler()
    sUrl = oParams.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    sPattern = '<a href="([^"]+)//([^"/]+)([^"]+)" target="_blank"><img class="sd'
    aResult = cParser().parse(sHtmlContent, sPattern)
    hosters = []
    if aResult[1]:
        for sHttp, sName, sUrl in aResult[1]:
            hoster = {}
            hoster['link'] = sHttp + '//' + sName + sUrl
            hoster['name'] = sName
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
