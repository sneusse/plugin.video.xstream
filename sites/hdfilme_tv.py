# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil
import re, json

# Plugin-Eigenschaften
SITE_IDENTIFIER = 'hdfilme_tv'
SITE_NAME = 'HDfilme'
SITE_ICON = 'hdfilme.png'

# Basis-URL's
URL_MAIN = 'http://hdfilme.tv/'
URL_MOVIES = URL_MAIN + 'movie-movies?'
URL_SHOWS = URL_MAIN + 'movie-series?'
URL_SEARCH = URL_MAIN + 'movie/search?key='

# Parameter für die Sortierung
URL_PARMS_ORDER_ID = 'order_f=id'
URL_PARMS_ORDER_ID_ASC = URL_PARMS_ORDER_ID +'&order_d=asc'
URL_PARMS_ORDER_NAME = 'order_f=name'
URL_PARMS_ORDER_NAME_ASC = URL_PARMS_ORDER_NAME +'&order_d=asc'

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)

    # GUI-Element erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Einträge anlegen
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showContentMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showContentMenu'), params)
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
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_ID)
    oGui.addFolder(cGuiElement('Neu hinzugefügt', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_NAME_ASC)
    oGui.addFolder(cGuiElement('Alphabetisch', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + URL_PARMS_ORDER_NAME_ASC)
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

    # Movie-Seite laden
    oRequestHandler = cRequestHandler(entryUrl)
    sHtmlContent = oRequestHandler.request()

    # Select für Generes Laden
    pattern = '<select[^>]*name="cat"[^>]*>(.*?)</select[>].*?'

    # Regex parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Nichts gefunden? => raus hier
    if not aResult[0]:
        return

    # Filter für Genres
    pattern = '<option[^>]*value="(\d[^ ]*)"[^>]*>(.*?)</option[>].*?'
    
    # Regex parsen
    aResult = cParser().parse(aResult[1][0], pattern)

    # Nichts gefunden? => raus hier
    if not aResult[0]:
        return

    # Alle Genres durchlaufen und Liste erzeugen
    for sID,sGenre in aResult[1]:
        params.setParam('sUrl',entryUrl + '&cat=' + sID)
        oGui.addFolder(cGuiElement(sGenre.strip(), SITE_IDENTIFIER, 'showEntries'), params)
    
    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # Aktuelle Seite ermitteln und ggf. URL anpassen
    iPage = int(params.getValue('page'))
    oRequest = cRequestHandler(entryUrl + '&per_page=' + str(iPage * 50) if iPage > 0 else entryUrl)

    # Daten ermitteln
    sHtmlContent = oRequest.request()
    
    # Prüfen ob es sich um einen Film oder um eine Serie handelt
    isTvshow = True if URL_SHOWS in entryUrl else False

    # Filter out the main section
    pattern = '<ul class="products row">.*?</ul>'
    aResult = cParser().parse(sHtmlContent, pattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Content festlegen der geparst werden soll
    sMainContent = aResult[1][0]

    # URL ermitteln
    pattern = '<div[^>]*class="box-product clearfix"[^>]*>\s*?'
    pattern += '<a[^>]*href="([^"]*)"[^>]*>.*?'

    # Rhumbnail ermitteln
    pattern += '<img[^>]*src="([^"]*)"[^>]*>.*?'

    # Name ermitteln
    pattern += '<div[^>]*class="popover-title"[^>]*>.*?'
    pattern += '<span[^>]*class="name"[^>]*>([^<>]*)</span>.*?'

    # Beschreibung ermitteln
    pattern += '<div[^>]*class="popover-content"[^>]*>\s*<p[^>]*>([^<>]*)</p>'

    # HTML parsen
    aResult = cParser().parse(sMainContent, pattern)

    # Kein Einträge gefunden? => Raus hier
    if not aResult[0]: 
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Listengröße ermitteln
    total = len (aResult[1])

    # Alle Ergebnisse durchlaufen
    for sUrl, sThumbnail, sName, sDesc in aResult[1]:
        # Bei Filmen das Jahr vom Title trennen
        aYear = re.compile("(.*?)\((\d*)\)").findall(sName)
        iYear = False
        for name, year in aYear:
            sName = name
            iYear = year
            break;

        # Listen-Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')

        # Bei Serien Title anpassen
        res = re.search('(.*?) staffel (\d+)', sName,re.I)
        if res:
            oGuiElement.setTVShowTitle(res.group(1))
            oGuiElement.setTitle('%s - Staffel %s' % (res.group(1),int(res.group(2))))

        # Thumbnail und Beschreibung für Anzeige anpassen
        sThumbnail = sThumbnail.replace('_thumb', '')
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()

        # Falls vorhanden Jahr ergänzen
        if iYear:
            oGuiElement.setYear(iYear)

        # Eigenschaften setzen und Listeneintrag hinzufügen
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setMediaType('tvshow' if isTvshow or res else 'movie')
        oGuiElement.setDescription(sDesc)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, True if isTvshow or res else False, total)

    # Pattern um die Aktuelle Seite zu ermitteln
    pattern = '<ul[^>]*class="pagination[^>]*>.*'
    pattern += '<li[^>]*class="active"[^>]*><a>(\d*)</a>.*</ul>'

    # Seite parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Falls ein Ergebniss gefunden wurden "Next-Page" ergänzen
    if aResult[0] and aResult[1][0]:
        params.setParam('page', int(aResult[1][0]))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)

    # Liste abschließen und View setzen
    if not sGui:
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()

def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # URL Anpassen um die Stream und nicht die Infos zu bekommen
    entryUrl = params.getValue('entryUrl').replace("-info","-stream")

    # Seite abrufen
    sHtmlContent = cRequestHandler(entryUrl).request()

    # Prüfen ob Episoden gefunden werden
    pattern = '<a[^>]*episode="([^"]*)"[^>]*href="([^"]*)"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)

    # Falls Episoden gefunden worden => Episodenauswahl vorschalten
    if aResult[0] and '-staffel-' in entryUrl:
        showEpisodes(aResult[1], params)
    else:
        return getHosters(entryUrl, params.getValue('sName'))

def showEpisodes(aResult, params):
    # GUI-Element erzeugen wenn nötig
    oGui = cGui()

    # Variable für Ansicht vorbereiten
    sTVShowTitle = params.getValue('TVShowTitle')
    sName = params.getValue('sName')
    iSeason = int(re.compile('.*?staffel\s*(\d+)').findall(sName.lower())[0])
    sThumbnail = params.getValue('sThumbnail')

    # Listengröße ermitteln
    total = len (aResult)

    # Alle Folgen durchlaufen und Einträge erzeugen
    for iEpisode, sUrl in aResult:
        sName = 'Folge ' + str(iEpisode)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'getHosters')
        oGuiElement.setMediaType('episode')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(iSeason)
        oGuiElement.setEpisode(iEpisode)
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sUrl', sUrl)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, False, total)

    # Ansicht auf "Episoden" setze
    oGui.setView('episodes')

    # Liste abschließen
    oGui.setEndOfDirectory()

def getHosters(sUrl =False, sName = False):
    # GUI-Element erzeugen wenn nötig
    oGui = cGui()

    #ParameterHandler erzeugen
    params = ParameterHandler()

    # URL und Name ermitteln falls nicht übergeben
    sUrl = sUrl if sUrl else params.getValue('sUrl')
    sName = sName if sName else params.getValue('sName')

    # Seite abrufen
    sHtmlContent = cRequestHandler(sUrl).request()

    # JSon mit den Links ermitteln
    pattern = 'var.*?(\[{"file":.*?\])'
    aResult = cParser().parse(sHtmlContent, pattern)

    # Nichts gefunden? => Raus hier
    if not aResult[0] or not aResult[1][0]: 
        logger.info("hoster pattern did not match")
        return False

    # hosterliste initialisieren
    hosters = []

    # Alle Einträge durchlaufen und Hostereintrag erstellen
    for entry in json.loads(aResult[1][0]):
        if 'file' not in entry or 'label' not in entry: continue
        sLabel = sName + ' - ' + entry['label'].encode('utf-8')
        hoster = dict()
        hoster['link'] = entry['file']
        hoster['name'] = sLabel
        #hoster['displayedName'] = sLabel
        hoster['resolveable'] = True
        hosters.append(hoster)

    # Sind Hoster vorhanden? => Nachfolgefunktion ergänzen
    if hosters:
        hosters.append('play')

    return hosters

def play(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not sUrl: sUrl = oParams.getValue('url')

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = True
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
    showEntries(URL_SEARCH + sSearchText.strip(), oGui)
