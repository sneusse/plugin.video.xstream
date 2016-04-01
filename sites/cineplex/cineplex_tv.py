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

SITE_IDENTIFIER = 'cineplex_tv'
SITE_NAME = 'Cineplex'
SITE_ICON = 'cineplex.png'

URL_MAIN = 'http://cineplex.tv/'
URL_CINEMA = URL_MAIN + 'filme_2015/'
URL_SERIE = URL_MAIN + 'serien/'
URL_SEARCH = URL_MAIN + 'index.php?story='

#GENRES

URL_GENRE_LIST = {'Abenteuer' : 'abenteuer/',
                  'Action' : 'action/',
                  'Animation' : 'animation/',
                  'Drama' : 'drama/',
                  'Fantasy' : 'fantasy/',
                  'Horror' : 'horror/',
                  'Krieg' : 'krieg/',
                  'Kriminal' : 'kriminal/',
                  'Komödie' : 'komoedie/',
                  'Romanze' : 'romanze/',
                  'Sci-Fi' : 'sci-fi/',
                  'Sport' : 'sport/',
                  'Thriller' : 'thriller/',
                  'Western' : 'western/'}


def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    #oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showTvShowMenu'))
    #oGui.addFolder(cGuiElement('Schauspieler', SITE_IDENTIFIER, 'showActor'))
    #oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()

    if not sSearchText: return
    _search(oGui, sSearchText)

def _search(oGui, sSearchText):
    # Keine Eingabe? => raus hier
    if not sSearchText: return

    # URL-Übergeben und Ergebniss anzeigen
    showEntries(URL_SEARCH + sSearchText.strip() + '&do=search&subaction=search')

def showMovieMenu():
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('sUrl', URL_CINEMA)
    oGui.addFolder(cGuiElement('Aktuelle Kinofilme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenreList'), params)

    oGui.setEndOfDirectory()

def showGenreList():

    oGui = cGui()

    for key in sorted(URL_GENRE_LIST):
        params = ParameterHandler()
        params.setParam('sUrl', (URL_MAIN + URL_GENRE_LIST[key]))
        oGui.addFolder(cGuiElement(key, SITE_IDENTIFIER, 'showEntries'), params)


    oGui.setEndOfDirectory()

def showEntries(entryUrl=False):
    oGui = cGui()

    params = ParameterHandler()

    if not entryUrl: entryUrl = params.getValue('sUrl')

    sHtmlContent = cRequestHandler(entryUrl).request()

    pattern = 'li_block_title"><img\ssrc="(.+?(?=")).+?<a\shref="(.+?)">(.+?)\s\('

    aResult = cParser().parse(sHtmlContent, pattern)

    if len(aResult) > 0:

        for result in aResult[1]:
            oGuiElement = cGuiElement(result[2], SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(URL_MAIN + result[0])
            params.setParam('entryUrl', result[1])
            params.setParam('sName', result[2])
            params.setParam('sThumbnail', result[0])
            oGui.addFolder(oGuiElement, params, bIsFolder = False)

        oGui.setEndOfDirectory()

        return

def showHosters():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')

    sHtmlContent = cRequestHandler(sUrl).request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = 'tab-pane\sfade(\sactive\sin)?"\sid="(.+?)"(.+?<\/div>)'
    aResult = cParser().parse(sHtmlContent, sPattern, ignoreCase=True)

    hosters = []

    if len(aResult[1]) > 0:

        for hoster in aResult[1]:
            hPattern = '(http.*?)"'
            hResult = cParser().parse(hoster[2], hPattern, ignoreCase=True)

            if len(hResult[1]) > 0:
                for link in hResult[1]:
                    temphoster = {}
                    temphoster['name'] = hoster[1]
                    temphoster['link'] = link
                    hosters.append(temphoster)

    if len(hosters) > 0:
        hosters.append('getHosterUrl')

    return hosters

def getHosterUrl(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not sUrl: sUrl = oParams.getValue('url')

    logger.info("url %s" % sUrl)

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)

    # Ergebniss zurückliefern
    return results