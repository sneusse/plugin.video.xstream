# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import cUtil
import re, json


SITE_IDENTIFIER = 'hdfilme_tv'
SITE_NAME = 'HDfilme.TV'
SITE_ICON = 'hdfilme.png'

URL_MAIN = 'http://hdfilme.tv/'
URL_LOGIN = URL_MAIN + 'login.html?'
URL_MOVIES = URL_MAIN + 'movie-movies?'
URL_CINEMA_MOVIES = URL_MAIN + 'movie-cinemas?'
URL_SHOWS = URL_MAIN + 'movie-series?'
URL_SEARCH = URL_MAIN + 'movie/search?key='

URL_ABENTEUER = URL_MOVIES + 'cat=72'
URL_ACTION = URL_MOVIES + 'cat=73'
URL_ANIMATION = URL_MOVIES + 'cat=74'
URL_DRAMA = URL_MOVIES + 'cat=62'
URL_FAMILIE = URL_MOVIES + 'cat=65'
URL_FANTASY = URL_MOVIES + 'cat=66'
URL_HORROR = URL_MOVIES + 'cat=69' 	
URL_KOMOEDIE = URL_MOVIES + 'cat=71'
URL_KRIEG = URL_MOVIES + 'cat=77'
URL_KRIMI = URL_MOVIES + 'cat=78'
URL_MARTIALARTS = URL_MOVIES + 'cat=79'
URL_MONUMENTALFILM = URL_MOVIES + 'cat=80'
URL_ROMANZE = URL_MOVIES + 'cat=83'
URL_SCIFI = URL_MOVIES + 'cat=84'
URL_SPIONAGE = URL_MOVIES + 'cat=86'
URL_THRILLER = URL_MOVIES + 'cat=88'
URL_WESTERN = URL_MOVIES + 'cat=92'

def load():
    oGui = cGui()
   
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_SHOWS + 'order_f=id&order_d=desc')
    oGui.addFolder(cGuiElement('Neu hinzugefügt', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SHOWS + 'order_f=name&order_d=desc')
    oGui.addFolder(cGuiElement('Alphabetisch', SITE_IDENTIFIER, 'showEntries'), params)

    oGui.setEndOfDirectory() 

def showMovieMenu():
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_CINEMA_MOVIES)
    oGui.addFolder(cGuiElement('Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre',SITE_IDENTIFIER,'showMovieGenre'))   
    
    oGui.setEndOfDirectory()     

def showMovieGenre():
    oGui = cGui()
    params = ParameterHandler()
    
    params.setParam('sUrl', URL_ABENTEUER)
    oGui.addFolder(cGuiElement('Abenteuer', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_ACTION)
    oGui.addFolder(cGuiElement('Action', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_ANIMATION)
    oGui.addFolder(cGuiElement('Animation', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_DRAMA)
    oGui.addFolder(cGuiElement('Drama', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_FAMILIE)
    oGui.addFolder(cGuiElement('Familie', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_FANTASY)
    oGui.addFolder(cGuiElement('Fantasy', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_HORROR)
    oGui.addFolder(cGuiElement('Horror', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_KOMOEDIE)
    oGui.addFolder(cGuiElement('Komödie', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_KRIEG)
    oGui.addFolder(cGuiElement('Krieg', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_KRIMI)
    oGui.addFolder(cGuiElement('Krimi', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MARTIALARTS)
    oGui.addFolder(cGuiElement('Martial Arts', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MONUMENTALFILM)
    oGui.addFolder(cGuiElement('Monumentalfilm', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_ROMANZE)
    oGui.addFolder(cGuiElement('Romanze', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SCIFI)
    oGui.addFolder(cGuiElement('Sci-Fi', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SPIONAGE)
    oGui.addFolder(cGuiElement('Spionage', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_THRILLER)
    oGui.addFolder(cGuiElement('Thriller', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_WESTERN)
    oGui.addFolder(cGuiElement('Western', SITE_IDENTIFIER, 'showEntries'), params)

    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    if iPage > 0:
        oRequest = cRequestHandler(entryUrl + '&per_page=' + str(iPage * 50))
    else:
        oRequest = cRequestHandler(entryUrl)

    sHtmlContent = oRequest.request()
    if URL_SHOWS in entryUrl:
        oGui.setView('tvshows')
    else:
        oGui.setView('movies')

    # Filter out the main section
    pattern = '<ul class="products row">.*?</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0] or not aResult[1][0]: return
    sMainContent = aResult[1][0]

    # Grab the link
    pattern = '<div[^>]*class="box-product clearfix"[^>]*>\s*?'
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
    for sUrl, sThumbnail, sName, sDesc in aResult[1]:
        # Grab the year (for movies)
        aYear = re.compile("(.*?)\((\d*)\)").findall(sName)
        iYear = False
        for name, year in aYear:
            sName = name
            iYear = year
            break;
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if iYear:
            oGuiElement.setYear(iYear)
        oGuiElement.setMediaType('movie')
        sThumbnail = sThumbnail.replace('_thumb', '')
        oGuiElement.setThumbnail(sThumbnail)
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()
        oGuiElement.setDescription(sDesc)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params)

    pattern = '<ul[^>]*class="pagination[^>]*>.*'
    pattern += '<li[^>]*class="active"[^>]*><a>(\d*)</a>.*</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and aResult[1][0]:
        params.setParam('page', int(aResult[1][0]))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    oGui.setEndOfDirectory()

def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl').replace("-info","-stream")
    oRequest = cRequestHandler(entryUrl)
    sHtmlContent = oRequest.request()
    # Check if the page contains episodes
    pattern = '<a[^>]*episode="([^"]*)"[^>]*href="([^"]*)"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0] and len(aResult[1]) > 1:
        showEpisodes(aResult[1], params)
    else:
        showLinks(entryUrl, params.getValue('sName'))

def showEpisodes(aResult, params):
    oGui = cGui()
    sName = params.getValue('sName')
    iSeason = int(re.compile('.*?staffel\s*(\d+)').findall(sName.lower())[0])
    sThumbnail = params.getValue('sThumbnail')
    oGui.setView('episodes')
    for iEpisode, sUrl in aResult:
        sName = 'Folge ' + str(iEpisode)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showLinks')
        oGuiElement.setSeason(iSeason)
        oGuiElement.setEpisode(iEpisode)
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sUrl', sUrl)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params)
    oGui.setEndOfDirectory()

def showLinks(sUrl =False, sName = False):
    oGui = cGui()
    params = ParameterHandler()
    sUrl = sUrl if sUrl else params.getValue('sUrl')
    sName = sName if sName else params.getValue('sName')
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    pattern = 'var config = .*?(\[.*?\])'            
    aResult = cParser().parse(sHtmlContent, pattern)

    if ((not 'http' in str(aResult)) or (not 'https' in str(aResult))):
        pattern = 'var newlink = (\[.*?\])'      
        aResult = cParser().parse(sHtmlContent, pattern)

    if not aResult[0] or not aResult[1][0]: return 
        
    for aEntry in json.loads(aResult[1][0]):
        if 'file' not in aEntry or 'label' not in aEntry: continue
        sLabel = sName + ' - ' + aEntry['label'].encode('utf-8')
        oGuiElement = cGuiElement(sLabel, SITE_IDENTIFIER, 'play')
        params.setParam('url', aEntry['file'])
        oGui.addFolder(oGuiElement, params, False)
    oGui.setEndOfDirectory()

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
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(oGui, sSearchText)

# Search using the requested string sSearchText
def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_SEARCH + sSearchText, oGui)
    oGui.setEndOfDirectory()
