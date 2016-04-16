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

# Plugin-Eigenschaften
SITE_IDENTIFIER = 'gute_filme_to'
SITE_NAME = 'Gute Filme'
SITE_ICON = 'gutefilme.png'

# Basis-URL's
URL_MAIN = 'http://www.gute-filme.to/'
URL_LIST = URL_MAIN + 'filmliste/grid/%s/4:6/title/ASC/'
URL_SEARCH = URL_MAIN + '?s=%s&searchsubmit=U'

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)

    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    params.setParam('sUrl', URL_LIST % "#")
    oGui.addFolder(cGuiElement("Alle Filme", SITE_IDENTIFIER, 'showEntriesFilmlist'), params)
    oGui.addFolder(cGuiElement('A-Z', SITE_IDENTIFIER, 'showFilmlist'))
    params.setParam('sTyp', "Genre")
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showYearOrGenreList'),params)
    params.setParam('sTyp', "Jahr")
    oGui.addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showYearOrGenreList'),params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Liste abschließen
    oGui.setEndOfDirectory()

def showFilmlist():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Zahlen von 0-9
    for number in range(0, 10):
        params.setParam('sUrl', URL_LIST % str(number))
        oGui.addFolder(cGuiElement(str(number), SITE_IDENTIFIER, 'showEntriesFilmlist'), params)

    # Alle Buchstaben von A-Z
    import string   
    for letter in string.uppercase[:26]:
        params.setParam('sUrl', URL_LIST % str(letter))
        oGui.addFolder(cGuiElement(letter, SITE_IDENTIFIER, 'showEntriesFilmlist'), params)
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showYearOrGenreList():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Seite laden
    sHtmlContent = cRequestHandler(URL_MAIN).request()

    # Genre-Liste ermitteln
    pattern = "<a[^>]*href=['\"][^'\"]*['\"][^>]*>%s</a><ul class=['\"]sub-menu['\"]>(.*?)</ul>" % params.getValue('sTyp')
    aResult = cParser().parse(sHtmlContent, pattern)

    # Wurde eine Navigation gefunden?
    if aResult[0]: 
        # HTML-Content für den nächsten Schritt anpassen
        sHtmlContent = aResult[1][0]

        # Filter für Genres
        pattern = "<a[^>]*href=['\"]([^'\"]*)['\"][^>]*>(.*?)</a></li>"
    
        # Regex parsen
        aResult = cParser().parse(sHtmlContent, pattern)

        # Nichts gefunden? => raus hier
        if not aResult[0]:
            return

        # Alle Genres durchlaufen und Liste erzeugen
        for sUrl, sTitle in aResult[1]:
            oOutParms = ParameterHandler()
            oOutParms.setParam('sUrl', sUrl)
            oGui.addFolder(cGuiElement(sTitle.strip(), SITE_IDENTIFIER, 'showEntries'), oOutParms)
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # Seite abrufen
    sHtmlContent = cRequestHandler(entryUrl).request()

    # URL und Title ermitteln
    pattern = "<article[^>]*class=['\"].*? (movie|page) .*?['\"][^>]*>.*?"
    pattern += "<a[^>]*href=['\"]([^'\"]*)['\"][^>]*>(.*?)</a>.*?"

    # Thumbnail ermitteln (Optinal da Teilweise nicht vorhanden)
    pattern += "(?:<img[^>]*src=['\"]([^'\"]*)\?fit.*?['\"][^>]*>.*?)?"

    # Beschreibung ermitteln (Optinal da Teilweise nicht vorhanden)
    pattern += "(?:<div[^>]*class=['\"]post-entry-content['\"][^>]*><p>(.*?)<.*?)?"
    
    # article-Tag abschließen
    pattern += "</article>"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Alle Ergebnisse durchlaufen
    for sLinkTyp ,sUrl, sName, sThumbnail, sDesc in aResult[1]:
        if sLinkTyp == "movie" :
            __addMovieEntry(oGui, sName, sUrl, sThumbnail, sDesc)

    # Next-Page einbauen
    __addNextPage(oGui,sHtmlContent,params,'showEntries')

    # Liste abschließen (wenn nötig)
    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()

def showEntriesFilmlist(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # Seite abrufen
    sHtmlContent = cRequestHandler(entryUrl).request()

    # Title und URL ermitteln
    pattern = "<div[^>]*id=['\"]wpmoly-movie-\d*['\"][^>]*>\s*?"
    pattern += "<a[^>]*title=['\"]([^'\"]*)['\"][^>]*href=['\"]([^'\"]*)['\"][^>]*>\s?"

    # Thumbnail ermitteln (Optinal da Teilweise nicht vorhanden)
    pattern += "(?:<img[^>]*src=['\"]([^'\"]*)\?fit.*?['\"][^>]*>.*?)?"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Alle Ergebnisse durchlaufen
    for sName, sUrl, sThumbnail in aResult[1]:
        __addMovieEntry(oGui, sName, sUrl, sThumbnail)

    # Next-Page einbauen
    __addNextPage(oGui,sHtmlContent,params,'showEntriesFilmlist')

    # Liste abschließen (wenn nötig)
    if not sGui:
        oGui.setView('movies')
        oGui.setEndOfDirectory()

def __addMovieEntry(oGui, sName, sUrl, sThumbnail, sDesc = ""):
    # Listen-Eintrag erzeugen
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showHosters')

    # Anzeigen-Eigenschaften setzen
    oGuiElement.setTitle(cUtil().unescape(sName.decode('utf-8')).encode('utf-8'))
    oGuiElement.setMediaType('movie')
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip())

    # Eigenschaften setzen und Listeneintrag hinzufügen
    oOutParms = ParameterHandler()
    oOutParms.setParam('entryUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutParms, bIsFolder = False)

def __addNextPage(oGui, sHtmlContent, params, function):
    # Seiten-Navigation ermitteln 
    pattern = "<ul[^>]*class=['\"]wpmoly page-numbers['\"][^>]*>(.*?)</ul>"
    aResult = cParser().parse(sHtmlContent, pattern)

    # Fallback für die Verschiedenen Varianten
    if not aResult[0]:
        # Seiten-Navigation ermitteln 
        pattern = "<p[^>]*class=['\"]navigation-links['\"][^>]*>(.*?)</p>"
        aResult = cParser().parse(sHtmlContent, pattern)

    # Wurde eine Navigation gefunden?
    if aResult[0]: 
        # HTML-Content für den nächsten Schritt anpassen
        sHtmlContent = aResult[1][0]

        # Seiten ermitteln
        pattern = "<a[^>]*href=['\"]([^'\"]*)['\"][^>]*>(\d+)</a>"
        aResult = cParser().parse(sHtmlContent, pattern)

        # Seiten gefunden?
        if aResult[0]:
            # Aktuelle Seite ermitteln
            currentPage = int(params.getValue('mediaTypePageId'))

            # Fallback für ersten Aufruf
            if currentPage == 0: currentPage = 1

            # Alle Seiten durchlaufen und 
            for sUrl, sPage in aResult[1]:
                # Seite ermitteln
                page = int(sPage)

                # Seite kleiner als die Aktuelle? => weiter machen
                if page <= currentPage: continue

                # "Next-Page"-Eintrage erstellen
                params.setParam('sUrl', sUrl)
                params.setParam('mediaTypePageId', page)
                oGui.addNextPage(SITE_IDENTIFIER, function, params)
                break

def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # URL ermitteln
    sUrl = params.getValue('entryUrl')

    # Seite Laden und anpassen
    sHtmlContent = cRequestHandler(sUrl).request()

    # JSon für die Hoster ermitteln
    sPattern = "<p><iframe[^>]src=['\"]([^'\"]*)['\"][^>]*>";
    aResult = cParser().parse(sHtmlContent, sPattern)

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []

    # JSon String festlegen
    if aResult[0]: 
        result = {}
        result['streamUrl'] = aResult[1][0]
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
    _search(False, sSearchText)

    #Liste abschließen
    oGui.setEndOfDirectory()

# Such-Funktion (z.b auch für Globale-Suche)
def _search(oGui, sSearchText):
    # Keine Eingabe? => raus hier
    if not sSearchText: return

    # URL-Übergeben und Ergebniss anzeigen
    showEntries(URL_SEARCH % sSearchText.strip(), oGui)
