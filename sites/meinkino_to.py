# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
from urlparse import urlparse
import json

SITE_IDENTIFIER = 'meinkino_to'
SITE_NAME = 'MeinKino'

URL_MAIN = 'http://meinkino.to/'
URL_NEW_FILME = URL_MAIN + 'filme?order=veroeffentlichung'
URL_FILME = URL_MAIN + 'filme'
URL_SERIE = URL_MAIN + 'tv'
URL_GET_URL = URL_MAIN + 'geturl/'

QUALITY_ENUM = {'240': 0, '360': 1, '480': 2, '720': 3, '1080': 4}

def load():
   logger.info("Load %s" % SITE_NAME)
   oGui = cGui()
   params = ParameterHandler()
   params.setParam('sUrl', URL_NEW_FILME)
   oGui.addFolder(cGuiElement('Neue Filme', SITE_IDENTIFIER, 'showEntries'), params)
   params.setParam('sUrl', URL_FILME)
   oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
   params.setParam('sUrl', URL_SERIE)
   oGui.addFolder(cGuiElement('TV-Serien', SITE_IDENTIFIER, 'showEntries'), params)
   oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl, ignoreErrors = (sGui is not False)).request()
    parser = cParser()
    pattern = '<a[^>]*href="([^"]+)id([^"]+)"[^>]*class="ml-name">([^"<]+).*?img*[^>]src="([^"]+).*?</a> ,([^<]+).*?IMDb:([^<]+).*?></span>([^<]+)'

    isMatch, aResult = parser.parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult)

    for sUrl, sId, sName, sThumbnail, sYear,IMDb, qualy in aResult:
        sFunction = "showHosters" if not "staffel" in sUrl else "showEpisodes"
        isTvshow = True if "staffel" in sUrl else False
        oGuiElement = cGuiElement(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'), SITE_IDENTIFIER, sFunction)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setYear(sYear)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', sUrl + 'id' + sId if isTvshow else URL_GET_URL + sId)
        params.setParam('sName', sName)
        params.setParam('Thumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    isMatchNextPage, sNextUrl = parser.parseSingleResult(sHtmlContent, '<link[^>]*rel="next"[^>]*href="([^"]+)')
    if isMatchNextPage:
        params.setParam('sUrl', sNextUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setView('tvshows' if 'staffel' in entryUrl else 'movies')
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('Thumbnail')
    sHtmlContent = cRequestHandler(sUrl).request()

    pattern = 'stream-id([^"]+)">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)    
   
    total = len (aResult)

    for sId, iEpisode in aResult:
        oGuiElement = cGuiElement('Folge ' + iEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('episode')
        oGuiElement.setEpisode(iEpisode)
        params.setParam('entryUrl', URL_GET_URL + sId)
        params.setParam('sName', 'Folge' + iEpisode)
        oGui.addFolder(oGuiElement, params, False, total)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def showHosters(): # dirty
    sUrl = ParameterHandler().getValue('entryUrl')
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry("X-Requested-With","XMLHttpRequest")
    oRequest.setRequestType(1)
    sJson = oRequest.request()
    
    if not sJson:
        return []

    hosters = []
    data = json.loads(sJson)

    # add main link
    if isinstance(data["url"], list):
        for urlData in data["url"]:
            hosters.append(__getHosterFromList(urlData))
    else:
        hosters.append(__getHosterEntry(data["url"]))

    # add alternative links
    if 'alternative' in data:
        for urlData in data["alternative"]:
            hosterData = data["alternative"][urlData]
            if isinstance(hosterData, list):
                for urlHosterData in hosterData:
                    hosters.append(__getHosterFromList(urlHosterData))
            else:
                hosters.append(__getHosterEntry(hosterData, urlData))

    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def __getHosterFromList(urlData, hostername=False):
    if not hostername:
        parsed_url = urlparse(urlData["link_mp4"])
        hostername = parsed_url.netloc

    hoster = dict()
    hoster['link'] = urlData["link_mp4"]
    hoster['name'] = hostername
    if urlData["quality"] in QUALITY_ENUM:
        hoster['quality'] = QUALITY_ENUM[urlData["quality"]]
    hoster['displayedName'] = '%sP (%s)' % (urlData["quality"], hostername)
    return hoster

def __getHosterEntry(sUrl, hostername=False):
    if not hostername:
        parsed_url = urlparse(sUrl)
        hostername = parsed_url.netloc

    hoster = dict()
    hoster['link'] = sUrl
    hoster['name'] = hostername
    hoster['displayedName'] = hostername.title()
    return hoster

def getHosterUrl(sUrl=False):
    if not sUrl: sUrl = ParameterHandler().getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results
