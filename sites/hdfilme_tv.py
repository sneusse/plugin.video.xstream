# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re, json

SITE_IDENTIFIER = 'hdfilme_tv'
SITE_NAME = 'HDfilme.tV'
SITE_ICON = 'hdfilme.png'

URL_MAIN = 'http://hdfilme.tv/'
URL_MOVIES = URL_MAIN + 'movie-movies'
URL_SHOWS = URL_MAIN + 'movie-series'
URL_SEARCH = URL_MAIN + 'movie/search?key='

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    if iPage > 0:
        oRequest = cRequestHandler(entryUrl + '?per_page=' + str(iPage * 50))
    else:
        oRequest = cRequestHandler(entryUrl)
    sHtmlContent = oRequest.request()

    if URL_SHOWS in entryUrl:
        contentType = 'tvshows'
        mediaType = 'tvshow'
        isFolder = True
    else:
        contentType = 'movies'
        mediaType = 'movie'
        isFolder = False

    # Filter out the main section
    pattern = '<ul class="products row">(.*?)</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0] or not aResult[1][0]: return
    sMainContent = aResult[1][0]

    # Grab the link
    pattern = '<div[^>]*class="box-product clearfix"[^>]*>\s*'
    pattern += '<a[^>]*href="([^"]*)"[^>]*>.*?'
    # Grab the thumbnail
    pattern += '<img[^>]*src="([^"]*)"[^>]*>.*?'
    # Grab the name
    pattern += '<div[^>]*class="popover-title"[^>]*>.*?'
    pattern += '<span[^>]*class="name"[^>]*>([^<>]*)</span>.*?'
    # Grab the description
    pattern += '<div[^>]*class="popover-content"[^>]*>\s*<p[^>]*>([^<>]*)</p>'
    
    aResult = cParser().parse(sMainContent, pattern)
    if not aResult[0]: return
    total = len (aResult[1])
    for sUrl, sThumbnail, sName, sDesc in aResult[1]:
        # Grab the year (for movies)
        aYear = re.compile("(.*?)\((\d*)\)").findall(sName)
        iYear = False
        for name, year in aYear:
            sName = name
            iYear = year
            break
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if mediaType == 'tvshow':
            res = re.search('(.*?) staffel (\d+)', sName,re.I)
            if res:           
                oGuiElement.setSeason(res.group(2)) 
                oGuiElement.setTVShowTitle(res.group(1))
                oGuiElement.setTitle('%s - Staffel %s' % (res.group(1),res.group(2)))
        if iYear:
            oGuiElement.setYear(iYear)
        oGuiElement.setMediaType(mediaType)
        sThumbnail = sThumbnail.replace('_thumb', '')
        oGuiElement.setThumbnail(sThumbnail)
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()
        oGuiElement.setDescription(sDesc)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isFolder, total)

    pattern = '<ul[^>]*class="pagination[^>]*>.*?'
    pattern += '<li[^>]*class="active"[^>]*><a>(\d*)</a>.*?</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and aResult[1][0]:
        params.setParam('page', int(aResult[1][0]))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    if sGui: return
    oGui.setView(contentType)
    oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl').replace("-info","-stream")
    oRequest = cRequestHandler(entryUrl)
    sHtmlContent = oRequest.request()
    # Check if the page contains episodes
    pattern = '<a[^>]*episode="([^"]*)"[^>]*href="([^"]*)"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and '-staffel-' in entryUrl or len(aResult[1]) > 1:
        showEpisodes(aResult[1], params)
    else:
        return getHosters(entryUrl, params.getValue('sName'))

def showEpisodes(aResult, params):
    oGui = cGui()
    sName = params.getValue('sName')
    iSeason = int(params.getValue('season'))
    sThumbnail = params.getValue('sThumbnail')
    for iEpisode, sUrl in aResult:
        sName = 'Folge ' + str(iEpisode)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'getHosters')
        oGuiElement.setSeason(iSeason)
        oGuiElement.setEpisode(iEpisode)
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sUrl', sUrl)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, False)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()

def getHosters(sUrl = False, sName = False):
    params = ParameterHandler()
    sUrl = sUrl if sUrl else params.getValue('sUrl')
    sName = sName if sName else params.getValue('sName')
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    pattern = '(\[{".*?}\])'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0] or not aResult[1][0]: 
        logger.info("hoster pattern did not match")
        return False
    hosters = []
    for entry in json.loads(aResult[1][0]):
        if 'file' not in entry or 'label' not in entry: continue
        sLabel = sName + ' - ' + entry['label'].encode('utf-8')
        hoster = dict()
        hoster['link'] = entry['file']
        hoster['name'] = sLabel
        #hoster['displayedName'] = sLabel
        hoster['resolveable'] = True
        hosters.append(hoster)
    if hosters:
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

# Show the search dialog, return/abort on empty input
def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)

# Search using the requested string sSearchText
def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH + sSearchText, oGui)
