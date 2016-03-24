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

# Basis-Einträge für xStream
SITE_IDENTIFIER = 'anime_loads'
SITE_NAME = 'Anime-Loads'
SITE_ICON = 'anime_loads.png'

# Links definieren
URL_MAIN = 'http://www.anime-loads.org/'
URL_SEARCH_ANIME = 'search?q=%s&type=anime'
URL_MOVIES = URL_MAIN + 'anime-movies/'
URL_MOVIES_ASC = URL_MOVIES + '?sort=title&order=asc'
URL_SERIES = URL_MAIN + 'anime-series/'
URL_SERIES_ASC = URL_SERIES + '?sort=title&order=asc'

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)
    
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Menü erzeugen
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Liste abschließen
    oGui.setEndOfDirectory()

def showMovieMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Parameter setzen
    params = ParameterHandler()
    params.setParam('mediaTypePageId', 1)
    params.setParam('sUrl', URL_MOVIES)

    # Menü erzeugen
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Neuste Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES_ASC)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showSeriesMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Parameter setzen
    params = ParameterHandler()
    params.setParam('mediaTypePageId', 1)
    
    # Menü erzeugen
    params.setParam('sUrl', URL_SERIES)
    oGui.addFolder(cGuiElement('Neuste Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIES_ASC)
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

# Sucher über UI
def showSearch():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # Tastatur anzeigen und Eingabe ermitteln
    sSearchText = oGui.showKeyBoard()

    # Keine Eingabe? => raus hier
    if not sSearchText: return
    
    # Suche durchführen
    _search(oGui, sSearchText)

    # Liste abschließen
    oGui.setEndOfDirectory()

# Such-Funktion (z.b auch für Globale-Suche)
def _search(oGui, sSearchText):
    # Keine Eingabe? => raus hier
    if not sSearchText: return
    
    # Suche durchführen
    oRequest = cRequestHandler(URL_SEARCH_ANIME % sSearchText)
    data = oRequest.request()
    
    # Ergebniss anzeigen
    showEntries(data, oGui)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(sContent = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # Je nach URL View setzen
    oGui.setView('tvshows' if URL_SERIES in params.getValue('sUrl') else 'movie')

    # Wurde kein Content übergeben? => Laden
    if sContent:
        sHtmlContent = sContent
    else:
        oRequestHandler = cRequestHandler(params.getValue('sUrl'))
        sHtmlContent = oRequestHandler.request()

    # Thumbnail ermitteln
    pattern = '<img[^>]*src="([^"]*)"[^>]*class="img-responsive[ ]img-rounded"[^>]*>.*?'
    # Links und Title ermitteln
    pattern += '<a[^>]*href="([^"]*)"[^>]*>(.*?)</a[>].*?'
    
    # Typ, Jahr und Anzahl der Episoden ermitteln
    pattern += '<a[^>]*><i[^>]*></i>(.*?)</a[>].*?'
    pattern += '<a[^>]*><i[^>]*></i>(.*?)</a[>].*?'
    pattern += '<span[^>]*><i[^>]*></i>(.*?)</span[>].*?'

    # Beschreibung ermitteln
    pattern += '<div[^>]*class="mt10"[^>]*>([^<>]*)</div>.*?'

    # Genre (wird aktuell nicht weiter benutzt)
    pattern += '<a[^>]*class="label[ ]label-info"[^>]*>([^<>]*)</a>'

    # Regex parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Nichts gefunden? => raus hier
    if not aResult[0]:
        return

    # Ergebnisse durchlaufen 
    for sThumbnail, sUrl, sName, sTyp, sYear, sEpisodes, sDesc, sGenre in aResult[1]:
        # Prüfen ob es sich um einen Film oder um eine Serie handelt
        isMovie = True if sTyp == 'Animie Film' else False

        # Decoding für die Beschreibung um Anzeifehler zu vermeiden
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()

        # Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('movie' if isMovie else 'tvshows')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc.strip())
        oGuiElement.setYear(sYear)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, bIsFolder = False)

    # Seiten-Navigation
    pattern = '<li><a[^>]*href="([^"]*)"[^>]*>(\d+)</a[>]</li>.*?'
    aResult = cParser().parse(sHtmlContent, pattern)
    
    # Wurde eine Navigation gefunden? => "Next-Page -->" einbauen
    if aResult[0]:
        # Aktuelle Seite ermitteln
        currentPage = int(params.getValue('mediaTypePageId'))
        
        # alle Ergebnisse durchlaufen
        for sUrl, sPage in aResult[1]:
            # Seite vom Ergebniss ermitteln
            page = int(sPage)

            # Falls die Seite kleiner ist => Weiter machen bis das nicht der Fall ist
            if page <= currentPage: continue
            
            # Eintrag erzeugen und Schleife verlassen
            params.setParam('sUrl', URL_MAIN + sUrl)
            params.setParam('mediaTypePageId', page)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
            break
    if not sGui:
        # List abschließen
        oGui.setEndOfDirectory()

# Hoster-Dialog anzeigen
def showHosters():
    params= ParameterHandler()
