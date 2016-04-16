# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import logger
from resources.lib.config import cConfig
import re, json

# Plugin-Eigenschaften
SITE_IDENTIFIER = 'ddl_me'
SITE_NAME = 'DirectDownLoad'
SITE_ICON = 'ddl.png'
SITE_SETTINGS = '<setting default="de.ddl.me" enable="!eq(-1,false)" id="ddl_me-domain" label="' + SITE_NAME + ' domain" type="labelenum" values="de.ddl.me|en.ddl.me" />'

# Settings Auslesen
oConfig = cConfig()
DOMAIN = oConfig.getSetting('ddl_me-domain')

# Basis-URL's
URL_MAIN = 'http://' + DOMAIN
URL_SEARCH = URL_MAIN + '/search_99/?q='
URL_MOVIES = URL_MAIN + '/moviez'
URL_SHOWS = URL_MAIN + '/episodez'
URL_TOP100 = URL_MAIN + '/top100/cover/'

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
    params.setParam('sUrl', URL_MOVIES)
    params.setParam('sTop100Type', 'movies')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    params.setParam('sTop100Type', 'tv')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_TOP100 + 'total/all/')
    oGui.addFolder(cGuiElement('Hall of Fame', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Liste abschließen
    oGui.setEndOfDirectory()

def showContentMenu():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Basis-URL ermitteln (Filme oder Serien)
    baseURL = params.getValue('sUrl')

    # Einträge anlegen
    oGui.addFolder(cGuiElement('Top 100',SITE_IDENTIFIER,'showTop100Menu'), params) 
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Letztes Update', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_BLOCKBUSTER)
    oGui.addFolder(cGuiElement('Blockbuster', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_IMDB_RATING)
    oGui.addFolder(cGuiElement('IMDB Rating', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_YEAR)
    oGui.addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + PARMS_GENRE_ALL + PARMS_SORT_LAST_UPDATE)
    oGui.addFolder(cGuiElement('Genre',SITE_IDENTIFIER,'showGenreList'), params)
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showTop100Menu():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Einträge anlegen
    params.setParam('sUrl',URL_TOP100 + 'today/' + params.getValue('sTop100Type'))
    oGui.addFolder(cGuiElement('Heute', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl',URL_TOP100 + 'month/' + params.getValue('sTop100Type'))
    oGui.addFolder(cGuiElement('Monat', SITE_IDENTIFIER, 'showEntries'), params)

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
    pattern = "<div[^>]*class='iwrap type_(\d*)'[^>]*>\s*?"
    pattern += "<a[^>]*title='([^']*)'*[^>]*href='([^']*)'*>.*?"

    # Thumbnail ermitteln
    pattern += "<img[^>]*src='([^']*)'[^>]*>.*?"

    # Jahr ermitteln
    pattern += "<span[^>]*class='bottomtxt'[^>]*>\s*?<i>(\d*)<span"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Fallback falls die Suche nur ein Ergebniss liefert
    if not aResult[0] or not aResult[1][0]: 
        pattern = "<title>(.*?)[(](\d*)[)].*?"

        # Thumbnail ermitteln
        pattern += "<img[^>]*class='detailCover'[^>]*src='([^']*)'[^>]*>.*?"

        # MediaTyp ermitteln
        pattern += "var[ ]mtype[ ]=[ ](\d*);"

        # HTML parsen
        aOneResult = cParser().parse(sHtmlContent, pattern)

        # Funktion verlassen falls keine Daten ermittelt werden konnten
        if not aOneResult[0] or not aOneResult[1][0]: 
            if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
            return

        # Alle Ergebnisse durchlaufen
        for sName, sYear, sThumbnail, smType in aOneResult[1]:
            # Unnötige Zusätze vom Namen entfernen
            sName = _stripTitle(sName)

            # Listen-Eintrag erzeugen
            oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')

            # Falls vorhanden Jahr ergänzen
            if sYear:
                oGuiElement.setYear(sYear)

            # Eigenschaften setzen und Listeneintrag hinzufügen
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('tvshow' if smType == "1" else 'movie')
            params.setParam('entryUrl', entryUrl)
            params.setParam('sName', sName)
            params.setParam('sThumbnail', sThumbnail)

            # Bei Serien erst Staffeln und Episode abfragen
            if smType == "1":
                oGuiElement.setFunction("showAllSeasons")
                oGui.addFolder(oGuiElement, params)
            else:
                oGui.addFolder(oGuiElement, params, bIsFolder = False)
        # Liste abschließen
        oGui.setEndOfDirectory()
        
        # Funktion verlassen
        return

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Alle Ergebnisse durchlaufen
    for smType, sName, sUrl, sThumbnail,sYear in aResult[1]:
        # Unnötige Zusätze vom Namen entfernen
        sName = _stripTitle(sName)

        # Listen-Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')

        # Falls vorhanden Jahr ergänzen
        if sYear:
            oGuiElement.setYear(sYear)

        # Eigenschaften setzen und Listeneintrag hinzufügen
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('tvshow' if smType == "1" else 'movie')
        params.setParam('entryUrl', URL_MAIN + sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)

        # Bei Serien erst Staffeln und Episode abfragen
        if smType == "1":
            oGuiElement.setFunction("showAllSeasons")
            oGui.addFolder(oGuiElement, params)
        else:
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
    if not sGui:
        oGui.setEndOfDirectory()

def showAllSeasons():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # View anpassen
    oGui.setView('seasons')

    # URL ermitteln
    sUrl = params.getValue('entryUrl')
   
    # Seite Laden und anpassen
    sHtmlContent = cRequestHandler(sUrl).request()

    # JSon für die Hoster ermitteln
    sPattern = "var[ ]subcats[ ]=[ ](.*?);";
    aResult = cParser().parse(sHtmlContent, sPattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # JSon-Daten Laden
    data = json.loads(aResult[1][0])

    # Array für die Seasons
    seasons = []

    # Alle Folgen durchlaufen
    for key, value in data.items():
        # Staffel-Nummer ermitteln
        SeasonsNr = int(value['info']['staffel'])

        # Zur Liste hinzufügen falls noch nicht in der Auflistung
        if SeasonsNr not in seasons:
            seasons.append(SeasonsNr)

    # Liste Sortieren
    seasons = sorted(seasons)

    # Thumbnail und Name ermitteln
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    # Seasons durchlaufen und Liste erstellen
    for iSeason in seasons:
        # Listen-Eintrag erzeugen
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showAllEpisodes')

        # Anzeigen-Eigenschaften setzen
        oGuiElement.setTitle("Staffel " + str(iSeason))
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(iSeason)
        oGuiElement.setMediaType('season')
        oGuiElement.setThumbnail(sThumbnail)

        # Eigenschaften setzen und Listeneintrag hinzufügen
        oOutParms = ParameterHandler()
        oOutParms.setParam('entryUrl', sUrl)
        oOutParms.setParam('sName', sName)
        oOutParms.setParam('sThumbnail', sThumbnail)
        oOutParms.setParam('iSeason', iSeason)
        oOutParms.setParam('sJson', aResult[1][0])
        oGui.addFolder(oGuiElement, oOutParms)

    #Liste abschließen
    oGui.setEndOfDirectory()

def showAllEpisodes():
    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # View anpassen
    oGui.setView('episodes')

    # Parameter ermitteln
    sUrl = params.getValue('entryUrl')
    iSeason = int(params.getValue('iSeason'))
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')
    sJson = params.getValue('sJson')

    # JSon-Daten Laden
    data = json.loads(sJson)

    # Array für die Seasons
    episodes = {}

    # Alle Folgen durchlaufen
    for key, value in data.items():
        # Staffel-Nummer ermitteln
        SeasonsNr = int(value['info']['staffel'])

        # Prüfen ob es sich um die Richtige Staffel handelt
        if SeasonsNr != iSeason:
            continue

        # Folge ermitteln
        episodeNr = int(value['info']['nr'])

        # Zur Liste hinzufügen falls noch nicht in der Auflistung
        if episodeNr not in episodes.keys():
            episodes.update({episodeNr : key})

    # Alle Einträge durchlaufen
    for iEpisodesNr, sEpisodesID in episodes.items():
        # Listen-Eintrag erzeugen
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showHosters')

        # Fallback Namen festlegen
        epiName = data[sEpisodesID]['info']['name'].encode('utf-8')

        # Name ermitteln
        sPattern = "(.*?)»";
        aResult = cParser().parse(epiName, sPattern)
        
        # Prüfen ob der Name geparst werden konnte
        if aResult[0]: 
            epiName = aResult[1][0]

        # Anzeigen-Eigenschaften setzen
        oGuiElement.setTitle(str(iEpisodesNr) + " - " + epiName)
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(iSeason)
        oGuiElement.setEpisode(iEpisodesNr)
        oGuiElement.setMediaType('episode')
        oGuiElement.setThumbnail(sThumbnail)

        # Eigenschaften setzen und Listeneintrag hinzufügen
        oOutParms = ParameterHandler()
        oOutParms.setParam('sJson', sJson)
        oOutParms.setParam('sJsonID', sEpisodesID)
        oGui.addFolder(oGuiElement, oOutParms, bIsFolder = False)

    #Liste abschließen
    oGui.setEndOfDirectory()

def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # Versuchen JSon vom ParameterHandler zu ermitteln
    sJson = params.getValue('sJson')

    # Prüfen ob JSon-Daten vorliegen
    if not sJson:
        # URL ermitteln
        sUrl = params.getValue('entryUrl')
   
        # Seite Laden und anpassen
        sHtmlContent = cRequestHandler(sUrl).request()

        # JSon für die Hoster ermitteln
        sPattern = "var[ ]subcats[ ]=[ ](.*?);";
        aResult = cParser().parse(sHtmlContent, sPattern)
    
        # JSon String festlegen
        if aResult[0]: 
            sJson = aResult[1][0]

    # hosterliste initialisieren
    hosters = []

    # Prüfen ob Daten gefunden wurden
    if sJson:
        # JSon-Daten Laden
        data = json.loads(sJson)

        # JSon-Key ermittlen
        sJsonID = params.getValue('sJsonID')
        
        # Falls keine ID übergeben wurden ersten Eintrag benutzen
        if not sJsonID:
            sJsonID = data.keys()[0]

        # Fallback für Serien (dort gibt es kein MultiPart)
        partCount = 1

        # Ermittelt ob der Film aus verschiedenen Parts besteht
        if '1' in data[sJsonID]:
            partCount = int(data[sJsonID]['1'])

        # Hoster durchlaufen
        for jHoster in data[sJsonID]['links']:
            # Alle Einträge der Hoste durchlaufen
            for jHosterEntry in data[sJsonID]['links'][jHoster]:
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

def _stripTitle(sName):
    # Unnötige Zusätze vom Namen entfernen
    sName = sName.replace("- Serie","")
    sName = sName.replace("(English)","")
    sName = sName.replace("(Serie)","")

    # Rückgabe
    return sName.strip()

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
    showEntries(URL_SEARCH + sSearchText.strip(), oGui)
