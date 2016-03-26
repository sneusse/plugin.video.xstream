# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import logger
import re, json

SITE_IDENTIFIER = 'ddl_me'
SITE_NAME = 'DirectDownLoad'
SITE_ICON = 'ddl.png'

URL_MAIN = 'http://de.ddl.me'
URL_SEARCH = URL_MAIN + '/search_99/?q='
URL_MOVIES = URL_MAIN + '/moviez'
URL_SHOWS = URL_MAIN + '/episodez'

# Basis-Genre (rest wird generiert)
PARMS_GENRE_ALL = "_00"

# Parameter für die Sortierung
PARMS_SORT_LAST_UPDATE = "_0"
PARMS_SORT_BLOCKBUSTER = "_1"
PARMS_SORT_IMDB_RATING = "_2"
PARMS_SORT_YEAR = "_3"

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)

    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Einträge anlegen
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    #oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'))
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Liste abschließen
    oGui.setEndOfDirectory()

def showMovieMenu():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Einträge anlegen
    params.setParam('sUrl', URL_MOVIES + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Letztes Update', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES + PARMS_GENRE_ALL + PARMS_SORT_BLOCKBUSTER)
    oGui.addFolder(cGuiElement('Nur Blockbuster', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES + PARMS_GENRE_ALL + PARMS_SORT_IMDB_RATING)
    oGui.addFolder(cGuiElement('Nach IMDB Rating', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES + PARMS_GENRE_ALL + PARMS_SORT_YEAR)
    oGui.addFolder(cGuiElement('Nach Jahr', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Genre',SITE_IDENTIFIER,'showGenreList'), params)   
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showGenreList():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL vom ParameterHandler ermitteln
    entryUrl = params.getValue('sUrl')

    # Seite laden
    sHtmlContent = cRequestHandler(entryUrl).request()

    # Filter für Genres
    pattern = '<a[^>]*href="([^"]*)".*?'
    pattern += '<i[^>]*class="fa fa-dot-circle-o".*?i>(.*?)</a>.*?'
    
    # Regex parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Nichts gefunden? => raus hier
    if not aResult[0]:
        return

    # Alle Genres durchlaufen und Liste erzeugen
    for sUrl, sTitle in aResult[1]:
        params.setParam('sUrl',URL_MAIN + sUrl)
        oGui.addFolder(cGuiElement(sTitle.strip(), SITE_IDENTIFIER, 'showEntries'), params)
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # Prüfen ob es sich um einen Film oder um eine Serie handelt
    isTvshow = True if URL_SHOWS in entryUrl else False

    # View ensprechent der URL anpassen
    oGui.setView('tvshows' if isTvshow else 'movies')

    # Seite abrufen
    sHtmlContent = cRequestHandler(entryUrl).request()

    # Title und URL ermitteln
    pattern = "<div[^>]*class='iwrap type_0'[^>]*>\s*?"
    pattern += "<a[^>]*title='([^']*)'*[^>]*href='([^']*)'*>.*?"

    # Thumbnail ermitteln
    pattern += "<img[^>]*src='([^']*)'[^>]*>.*?"

    # Jahr ermitteln
    pattern += "<span[^>]*class='bottomtxt'[^>]*>\s*?<i>(\d*)<span"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Fallback falls die Suche nur ein Ergebniss liefert
    if not aResult[0] or not aResult[1][0]: 
        pattern = "<h1[^>]*id='itemType'[^>]*>(.*?)[(](\d*).*?"

        # Thumbnail ermitteln
        pattern += "<img[^>]*src='([^']*)'[^>]*>.*?"

        # HTML parsen
        aOneResult = cParser().parse(sHtmlContent, pattern)

        # Funktion verlassen falls keine Daten ermittelt werden konnten
        if not aOneResult[0] or not aOneResult[1][0]: 
            oGui.showInfo('xStream1','Es wurde kein Eintrag gefunden')
            return
        
        # Alle Ergebnisse durchlaufen
        for sName, sYear, sThumbnail in aOneResult[1]:
            # Listen-Eintrag erzeugen
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')

            # Falls vorhanden Jahr ergänzen
            if sYear:
                oGuiElement.setYear(sYear)

            # Eigenschaften setzen und Listeneintrag hinzufügen
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
            params.setParam('entryUrl', entryUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)
            oGui.addFolder(oGuiElement, params, bIsFolder = False)
        # Liste abschließen
        oGui.setEndOfDirectory()
        
        # Funktion verlassen
        return

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Alle Ergebnisse durchlaufen
    for sName, sUrl, sThumbnail,sYear in aResult[1]:
        # Listen-Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')

        # Falls vorhanden Jahr ergänzen
        if sYear:
            oGuiElement.setYear(sYear)

        # Eigenschaften setzen und Listeneintrag hinzufügen
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', URL_MAIN + sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, bIsFolder = False)

    # Seiten-Navigation ermitteln 
    pattern = "<div[^>]*class='paging'[^>]*>(.*?)</div>"
    aResult = cParser().parse(sHtmlContent, pattern)

    # Wurde eine Navigation gefunden?
    if aResult[0]: 
        # HTML-Content für den nächsten Schritt anpassen
        sHtmlContent = aResult[1][0]

        # Seiten ermitteln
        pattern = "<a[^>]href='([^']*)'[^>]*>(\d)<[^>]*>"
        aResult = cParser().parse(sHtmlContent, pattern)

        # Seiten gefunden?
        if aResult[0]:
            # Aktuelle Seite ermitteln
            currentPage = int(params.getValue('mediaTypePageId'))

            # Alle Seiten durchlaufen und 
            for sUrl, sPage in aResult[1]:
                # Seite ermitteln
                page = int(sPage)

                # Seite kleiner als die Aktuelle? => weiter machen
                if page <= currentPage: continue

                # "Next-Page"-Eintrage erstellen
                params.setParam('sUrl', URL_MAIN + sUrl)
                params.setParam('mediaTypePageId', page)
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
                break

    # Liste abschließen
    oGui.setEndOfDirectory()

def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln
    sUrl = params.getValue('entryUrl')
   
    # Seite Laden und anpassen
    sHtmlContent = cRequestHandler(sUrl).request()

    # JSon für die Hoster ermitteln
    sPattern = "var[ ]subcats[ ]=[ ](.*?);";
    aResult = cParser().parse(sHtmlContent, sPattern)

    # hosterliste initialisieren
    hosters = []

    # Prüfen ob Daten gefunden wurden
    if aResult[0]: 
        # JSon-Daten Laden
        data = json.loads(aResult[1][0])

        # Ermittelt ob der Film aus verschiedenen Parts besteht
        partCount = int(data[data.keys()[0]]['1'])

        # Hoster durchlaufen
        for jHoster in data[data.keys()[0]]['links']:
            # Alle Einträge der Hoste durchlaufen
            for jHosterEntry in data[data.keys()[0]]['links'][jHoster]:
                # Nur Einträge beachten die auch Streams sind
                if jHosterEntry[5] == 'stream':
                    hoster = {}
                    if partCount > 1:
                        hoster['displayedName'] = jHoster + ' - Part ' + jHosterEntry[0]
                    hoster['link'] = jHosterEntry[3]
                    hoster['name'] = jHoster
                    hosters.append(hoster)

    # Sind Hoster vorhanden? => Nachfolgefunktion ergänzen
    if len(hosters) > 0:
        hosters.append('getHosterUrl')

    # Rückgabe
    return hosters
  
def getHosterUrl(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not sUrl: sUrl = oParams.getValue('url')

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)

    # Ergebniss zurückliefern
    return results

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

# Such-Funktion (z.b auch für Globale-Suche)
def _search(oGui, sSearchText):
    # Keine Eingabe? => raus hier
    if not sSearchText: return

    # URL-Übergeben und Ergebniss anzeigen
    showEntries(URL_SEARCH + sSearchText.strip(), oGui)
