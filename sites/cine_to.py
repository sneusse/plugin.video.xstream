# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re, json

SITE_IDENTIFIER = 'cine_to'
SITE_NAME = 'Cine.to'
SITE_ICON = 'cine_to.png'

URL_PROTOCOL = 'https:'
URL_MAIN = URL_PROTOCOL + '//cine.to'
URL_SEARCH = URL_PROTOCOL + '//cine.to/request/search'
URL_LINKS = URL_PROTOCOL + '//cine.to/request/links'
URL_OUT = URL_PROTOCOL + '//cine.to/out/%s'

SEARCH_DICT = {'kind':'all', 'genre':'0', 'rating':'1', 'year[]': ['1913', '2016'], 'term':'', 'page':'1', 'count' : '25'}
QUALITY_ENUM = {'SD':3,'HD':4}

def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    params = ParameterHandler()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'searchRequest'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def searchRequest(dictFilter = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()

    dictFilter = {}
    for (prop, val) in SEARCH_DICT.items():
        parmVal = params.getValue(prop)
        dictFilter[prop] = parmVal if parmVal else val
        params.setParam(prop, val)

    oRequest = _getRequestHandler(URL_SEARCH)
    for (prop, val) in dictFilter.items():
        oRequest.addParameters(prop,val)
    oResponse = json.loads(oRequest.request())

    if 'entries' not in oResponse or len(oResponse['entries']) == 0:
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    total = len (oResponse['entries'])
    for aEntry in oResponse['entries']:
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showHosters')
        oGuiElement.setTitle(aEntry['title'].encode('utf-8'))
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(URL_PROTOCOL + aEntry['cover'])
        oGuiElement.setYear(aEntry['year'])
        oOutParms = ParameterHandler()
        oOutParms.setParam('imdbID', aEntry['imdb'])
        oGui.addFolder(oGuiElement, oOutParms, False, total)

    if int(oResponse['current']) < int(oResponse['pages']):
        params.setParam('page', int(oResponse['current']) + 1)
        oGui.addNextPage(SITE_IDENTIFIER, 'searchRequest', params)

    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    imdbID = params.getValue('imdbID')

    if not imdbID: return

    oRequest = _getRequestHandler(URL_LINKS)
    oRequest.addParameters('ID', imdbID)
    oRequest.addParameters('lang','de')
    oResponse = json.loads(oRequest.request())

    if 'links' not in oResponse or len(oResponse['links']) == 0:
        return

    hosters = []
    for aEntry in oResponse['links']:
        hoster = dict()
        if oResponse['links'][aEntry][0].upper() in QUALITY_ENUM:
            hoster['quality'] = QUALITY_ENUM[oResponse['links'][aEntry][0]]
        hoster['link'] = URL_OUT % oResponse['links'][aEntry][1]
        hoster['name'] = aEntry
        hoster['displayedName'] = '%s - Quality: %s' % (aEntry, oResponse['links'][aEntry][0])
        hosters.append(hoster)

    if hosters:
        hosters.append('play')
    return hosters

def play(sUrl = False):
    if not sUrl: sUrl = oParams.getValue('url')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.request()
    sUrl = oRequestHandler.getRealUrl() # get real url from out-page

    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def _getRequestHandler(sUrl):
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('X-Requested-With','XMLHttpRequest')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    return oRequest

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    dictSearch = SEARCH_DICT
    dictSearch['term'] = sSearchText.strip()
    searchRequest(dictSearch, oGui)

