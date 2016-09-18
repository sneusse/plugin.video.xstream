# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
from cCFScrape import cCFScrape
import re, json

SITE_IDENTIFIER = 'tata_to'
SITE_NAME = 'Tata'
SITE_ICON = 'tata.png'

URL_MAIN = 'http://www.tata.to/'
URL_MOVIES = URL_MAIN + 'filme?type=filme'
URL_SHOWS = URL_MAIN + 'filme?type=tv'
URL_SEARCH = URL_MAIN + 'filme?suche=%s&type=alle'

URL_PARMS_ORDER_ID = '&order=neueste'
URL_PARMS_ORDER_MOSTVIEWED = '&order=ansichten'
URL_PARMS_ORDER_MOSTRATED = '&order=ratingen'
URL_PARMS_ORDER_TOPIMDB = '&order=imdb'
URL_PARMS_ORDER_RELEASEDATE = '&order=veröffentlichung'

def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showContentMenu'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showContentMenu():
    oGui = cGui()
    params = ParameterHandler()
    baseURL = params.getValue('sUrl')

    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_ID)
    oGui.addFolder(cGuiElement('Neuste', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_MOSTVIEWED)
    oGui.addFolder(cGuiElement('Am häufigsten gesehen', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_MOSTRATED)
    oGui.addFolder(cGuiElement('Am meisten bewertet', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_TOPIMDB)
    oGui.addFolder(cGuiElement('Top IMDb', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_RELEASEDATE)
    oGui.addFolder(cGuiElement('Veröffentlichungsdatum', SITE_IDENTIFIER, 'showEntries'), params) 
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()

    if not entryUrl: entryUrl = params.getValue('sUrl')

    oRequest = cRequestHandler(entryUrl)
    sHtmlContent = oRequest.request()
    pattern = '<div[^>]*class="ml-item-content"[^>]*>.*?' # start element
    pattern += '<a[^>]*href="([^"]*)"[^>]*>.*?' # url
    pattern += '(?:<span[^>]*class="quality-label (\w+)"[^>]*>.*?)?' # quality
    pattern += '<img[^>]*src="([^"]*)"[^>]*>.*?' # thumbnail
    pattern += '(?:<span[^>]*class="season-label"[^>]*>.*?<span[^>]*class="el-num"[^>]*>\s+(\d+)\s+</span>.*?)?' # season
    pattern += '</a>.*?' # end link
    pattern += '<h\d+>(.*?)</h\d+>.*?' # title
    pattern += '(?:<div[^>]*class="caption-description"[^>]*>(.*?)</div>.*?)' # description
    parser = cParser()
    aResult = parser.parse(sHtmlContent, pattern)

    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (aResult[1])
    for sUrl, sQuality, sThumbnail, sSeason, sName, sDesc in aResult[1]:
        isTvshow = True if sSeason else False

        sName = cUtil().unescape(sName).strip()
        sThumbnail = cCFScrape().createUrl(sThumbnail, oRequest)
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()
        
        sUrl = sThumbnail.replace('https:','http:')
        sThumbnail = sThumbnail.replace('https:','http:')

        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if isTvshow:
            res = re.search('(.*?)\s(?:Staffel \d+ Folge \d+\s+)?', sName, re.I)
            if res:
                sName = res.group(1)
            oGuiElement.setTVShowTitle(sName)
            oGuiElement.setTitle('%s - Staffel %s' % (sName, sSeason))
            params.setParam('sSeason', sSeason)

        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        oGuiElement.setDescription(sDesc)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('isTvshow', isTvshow)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    aResult = parser.parse(sHtmlContent, '<li[^>]*class="active".*?<a[^>]*href="([^"]*)"[^>]*>\d+</a>')
    if aResult[0] and aResult[1][0]:
        params.setParam('sUrl', aResult[1][0].replace('https:','http:'))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if not sGui:
        oGui.setView('tvshows' if 'type=tv' in entryUrl else 'movies')
        oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    isTvshowEntry = params.getValue('isTvshow')

    if isTvshowEntry == 'True':
        sHtmlContent = cRequestHandler(entryUrl).request()
        aResult = cParser().parse(sHtmlContent, '<li[^>].*?<a[^>]*href="([^"]*)"[^>]*>(\d+)</a>')
        if aResult[0]:
            showEpisodes(aResult[1], params)
    else:
        return getHosters(entryUrl)

def showEpisodes(aResult, params):
    oGui = cGui()

    sTVShowTitle = params.getValue('TVShowTitle')
    sName = params.getValue('sName')
    sThumbnail = params.getValue('sThumbnail')
    sSeason = params.getValue('sSeason')

    total = len (aResult)
    for sUrl, iEpisode in aResult:
        sName = 'Folge ' + str(iEpisode)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'getHosters')
        oGuiElement.setMediaType('episode')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(iEpisode)
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sUrl', sUrl)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, False, total)

    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def getHosters(sUrl = False):
    params = ParameterHandler()
    sUrl = sUrl if sUrl else params.getValue('sUrl')
    sHtmlContent = cRequestHandler(sUrl).request()

    pattern = '<div[^>]*data-url="([^"]*)"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)

    hosters = []
    if aResult[0] and aResult[1][0]:
        hoster = dict()
        hoster['link'] = aResult[1][0].replace('https:','http:')
        hoster['name'] = SITE_NAME
        hoster['resolveable'] = True
        hosters.append(hoster)
        hosters.append('play')
    return hosters

def play(sUrl = False):
    oParams = ParameterHandler()
    if not sUrl: sUrl = oParams.getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = True
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