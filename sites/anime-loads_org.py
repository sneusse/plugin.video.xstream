# -*- coding: utf-8 -*-
import json
import time
import re
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig

# Basis-Einträge für xStream
SITE_IDENTIFIER = 'anime-loads_org'
SITE_NAME = 'AnimeLoads'
SITE_ICON = 'anime-loads.png'

# Links definieren
URL_MAIN = 'http://www.anime-loads.org/'
URL_SEARCH = URL_MAIN + 'search?q=%s'
URL_MOVIES = URL_MAIN + '%s-movies/'
URL_MOVIES_ASC = URL_MOVIES + '?sort=title&order=asc'
URL_SERIES = URL_MAIN + '%s-series/'
URL_SERIES_ASC = URL_SERIES + '?sort=title&order=asc'

# Liste der Untersützten Typen
SUPP_TYPES = [ "anime", "asia", "hentai" ]

def load():
    # Logger-Eintrag
    logger.info("Load %s" % SITE_NAME)

    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Menü erzeugen
    params.setParam('sType', "anime")
    oGui.addFolder(cGuiElement('Anime', SITE_IDENTIFIER, 'showBasicMenu'), params)
    params.setParam('sType', "asia")
    oGui.addFolder(cGuiElement('Asia', SITE_IDENTIFIER, 'showBasicMenu'), params)
    if showAdult():
        params.setParam('sType', "hentai")
        oGui.addFolder(cGuiElement('Hentai', SITE_IDENTIFIER, 'showHentaiMenu'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))

    # Liste abschließen
    oGui.setEndOfDirectory()

def showBasicMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Menü erzeugen
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'), params)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showHentaiMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # Typ ermitteln
    sType = params.getValue('sType')

    # Menü erzeugen
    params.setParam('sUrl', URL_MAIN + sType)
    oGui.addFolder(cGuiElement('Neuste Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN + sType + '/?sort=title&order=asc')
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showMovieMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # Typ ermitteln
    sType = params.getValue('sType')

    # Menü erzeugen
    params.setParam('sUrl', URL_MOVIES % sType)
    oGui.addFolder(cGuiElement('Neuste Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES_ASC % sType)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showSeriesMenu():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Typ ermitteln
    sType = params.getValue('sType')

    # Menü erzeugen
    params.setParam('sUrl', URL_SERIES  % sType)
    oGui.addFolder(cGuiElement('Neuste Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIES_ASC  % sType)
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showEntries'), params)

    # Liste abschließen
    oGui.setEndOfDirectory()

def showEntries(entryUrl = False, sGui = False):
    # GUI-Element erzeugen wenn nötig
    oGui = sGui if sGui else cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not entryUrl: entryUrl = params.getValue('sUrl')

    # 'safe_search' entsprechend der xStream Einstellung setzen
    safeSearchUrl = entryUrl + ('&' if '?' in entryUrl else '?') + 'safe_search=' + str(int(showAdult()))

    # HTML-Laden
    sHtmlContent = _getRequestHandler(safeSearchUrl, True).request()

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
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Typ ermitteln
    sType = params.getValue('sType')

    # Prüfen ob es sich um einen Film oder um eine Serie handelt
    isTvshow = True if (URL_SERIES % sType) in entryUrl else False

    # Listengröße ermitteln
    total = len (aResult[1])

    # Ergebnisse durchlaufen
    for sThumbnail, sUrl, sName, sKind, sYear, sEpisodes, sDesc, sGenre in aResult[1]:
        # Typ des Eintrags anpassen
        sKind = sKind.strip().lower()

        # Name des Typs ermitteln
        sKindName = re.compile('\A(\w+)[ ]?').findall(sKind)[0]
        
        # Wird der Typ nicht unterstüzt nicht auflisten (z.b Soundtracks, Manga usw.)
        if sKindName not in SUPP_TYPES:
            continue

        # Prüfen ob es sich um einen Film oder um eine Serie handelt
        isMovie = True if sKind.endswith('film')  or ' ' not in sKind else False

        # Decoding für die Beschreibung um Anzeifehler zu vermeiden
        sDesc = cUtil().unescape(sDesc.decode('utf-8')).encode('utf-8').strip()

        # Eintrag erzeugen
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showReleases')
        oGuiElement.setMediaType('movie' if isMovie else 'tvshow')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc.strip())
        oGuiElement.setYear(sYear)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, True, total)

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

    # List abschließen
    if not sGui:
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()

def showReleases():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Variable für Ansicht vorbereiten
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    # Seite laden
    sHtmlContent = _getRequestHandler(params.getValue('entryUrl'), True).request()

    # ReleaseId und Name ermitteln
    pattern = "<a[^>]*href=['\"]#stream_(\d+)['\"][^>]*>.*?</i>(.*?)"

    # Sprache ermitteln (Optional)
    pattern += "(?:<i[^>]*class=['\"].*?flag-(\w+)['\"][^>]*>.*?)?"
    
    # Untertiel ermitteln (Optional) und Pattern schließn
    pattern += "(?:[|]\s<i[^>]*class=['\"].*?flag-(\w+)['\"][^>]*>.*?)?</li>"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Funktion verlassen falls keine Daten ermittelt werden konnten
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Listengröße ermitteln
    total = len(aResult[1])

    # alle Ergebnisse durchlaufen
    for sReleaseId, sReleaseName, sLang, sSubLang in aResult[1]:
        # Alle Streams des jeweiligen Releases ermitteln
        aStreams = cParser().parse(sHtmlContent, "id=['\"]streams_episodes_%s_\d['\"]" % sReleaseId)

        # Kein Episoden verfügbar? => weiter machen
        if not aResult[0] or not aResult[1][0]: 
            continue

        # unnötige Leerzeichen entfernen (falls vorhanden)
        sReleaseName = sReleaseName.strip()

        # Sprache ergänzen wenn möglich
        if sLang and sSubLang:
            sReleaseName += " (%s | %s)" % (sLang.upper(),sSubLang.upper())
        elif sLang:
            sReleaseName += " (%s)" % (sLang.upper())

        # Eintrag erzeugen
        oGuiElement = cGuiElement(sReleaseName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('iReleaseId', int(sReleaseId))

        # Episoden Streams verfügbar? => Liste anzeigen 
        if len(aStreams[1]) > 1:
            oGuiElement.setFunction("showEpisodes")
            oGui.addFolder(oGuiElement, params, True, total)
        else:
            params.setParam('iEpisodeId', 0)
            oGui.addFolder(oGuiElement, params, False, total)

    #Liste abschließen
    oGui.setEndOfDirectory()

def showEpisodes():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Seite laden (ungecached)
    sHtmlContent = _getRequestHandler(params.getValue('entryUrl')).request()

    # Pattern zum ermitteln der EpisodeId
    pattern = "<a[^>]*href=['\"]#streams_episodes_%d_(\d+)['\"][^>]*>.*?" % int(params.getValue('iReleaseId'))

    # Seriennummer und Name ermitteln
    pattern += "<strong>(\d+)</strong>(.*?)</span>"

    # HTML parsen
    aResult = cParser().parse(sHtmlContent, pattern)

    # Kein Episoden verfügbar? => weiter machen
    if not aResult[0] or not aResult[1][0]: 
        oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    # Variable für Ansicht vorbereiten
    sThumbnail = params.getValue('sThumbnail')
    sName = params.getValue('sName')

    # Listengröße ermitteln
    total = len(aResult[1])

    # alle Ergebnisse durchlaufen
    for sEpisodeId, sNumber, sEpisodName in aResult[1]:
        oGuiElement = cGuiElement(str(int(sNumber)) + " - " + sEpisodName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setMediaType('episode')
        oGuiElement.setEpisode(int(sNumber))
        oGuiElement.setThumbnail(sThumbnail)
        params.setParam('iEpisodeId', int(sEpisodeId))
        oGui.addFolder(oGuiElement, params, False, total)

    # Ansicht auf "Episoden" setze
    oGui.setView('episodes')

    #Liste abschließen
    oGui.setEndOfDirectory()

# Hoster-Dialog anzeigen
def showHosters():
    # ParameterHandler erzeugen
    params = ParameterHandler()

    # Seite laden (ungecached)
    sHtmlContent = _getRequestHandler(params.getValue('entryUrl')).request()

    # UserID ermitteln
    pattern = "'&ud=(.*?)\">"
    aUdResult = cParser().parse(sHtmlContent, pattern)

    # data-enc für den jeweiligen Eintrag ermitteln
    pattern = 'id="streams_episodes_%d_%d"\sdata-enc="(.+?)"' % (int(params.getValue('iReleaseId')),int(params.getValue('iEpisodeId')))
    aResult = cParser().parse(sHtmlContent, pattern)

    # Hosterliste initalisieren
    hosters = []

    # Liegen beide Einträge vor => Link ermitteln
    if aUdResult[0] and aResult[0]:
        hosters = _decryptLink(aResult[1][0], aUdResult[1][0])

    # Hoster Liste zurückgeben
    return hosters

def getHosterUrl(sUrl = False):
    #ParameterHandler erzeugen
    oParams = ParameterHandler()

    # URL ermitteln falls nicht übergeben
    if not sUrl: sUrl = oParams.getValue('url')

    # Array mit einem Eintrag für Hosterliste erzeugen (sprich direkt abspielen)
    results = []
    result = {}
    result['streamUrl'] = _resolveLeaveLink(sUrl)
    result['resolved'] = False

    # Konnte die URL ermittelt werden? => Zur List hinzufügen
    if result['streamUrl']:
        results.append(result)

    # Ergebniss zurückliefern
    return results

# Sucher über UI
def showSearch():
    # Gui-Elemet erzeugen
    oGui = cGui()

    # ParameterHandler erzeugen
    params = ParameterHandler()
    
    # Tastatur anzeigen und Eingabe ermitteln
    sSearchText = oGui.showKeyBoard()

    # Keine Eingabe? => raus hier
    if not sSearchText: return
    
    # Typ ermitteln
    sType = params.getValue('sType')

    # Typ ergänzen
    if sType:
        sSearchText = sSearchText.strip() + "&type="+sType

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

# Prüfen ob Adult gezeigt werden soll
def showAdult():
    oConfig = cConfig()
    if oConfig.getSetting('showAdult')=='true':    
        return True
    return False

'''
Capatcha und Leaver verarbeitung
'''

def _decryptLink(enc, ud):
    # Versuchen JSon direkt zu bekommen
    response = _sendEnc(enc, ud)

    # Kein Folge? => Capatcha lösen lassen
    if 'code' in response and response['code'] == 'error':
        token = _uncaptcha()
        if token:
            response = _sendEnc(enc, ud, token)

    # Hosterliste initialisieren
    hosters = []

    # Alle Hoster und die jeweiligen Links durchlaufen
    for entry in response['content']:
        for item in entry['links']:
            hoster ={}
            hoster['link'] = item['link']
            hoster['name'] = entry['hoster_name']
            if 'part' in item:
                hoster['displayedName'] = '%s - Part %s' % (entry['hoster_name'],item['part'])
            hosters.append(hoster)

    # Sind Hoster vorhanden? => Nachfolgefunktion ergänzen
    if len(hosters) > 0:
        hosters.append('getHosterUrl')

    # Rückgabe
    return hosters

def _resolveLeaveLink(link):
    # Leave-Link aufrufen
    sHtmlContent = _getRequestHandler(URL_MAIN + 'leave/' + link).request()

    # Entgültigen-Link ermitteln
    sPattern = "link\s+=\s'(.*?)',"
    aResult = cParser().parse(sHtmlContent, sPattern)

    # Link gefunden? => Link verfolgen und Redirect ermitteln
    if aResult[0]:
        # Fuck this... Sonnst gehts nicht -.-
        time.sleep(15)

        # Link verfolgen und Redirect zurückgeben
        oRequestHandler = _getRequestHandler(aResult[1][0])
        oRequestHandler.request()
        return oRequestHandler.getRealUrl()

def _sendEnc(enc, ud, response = None):
    # Cookies ermitteln
    _getRequestHandler('%sassets/pub/js/userdata?ud=%s' % (URL_MAIN, ud)).request()

    # Cookie anpassen und captcha AJax zum jeweiligen Link ausführen
    oRequestHandler = _getRequestHandler(URL_MAIN + 'ajax/captcha')
    oRequestHandler.addParameters('enc', enc)
    oRequestHandler.addParameters('response', (response if response else 'nocaptcha'))

    # Rückgabe-JSon lesen
    return json.loads(oRequestHandler.request())

def _uncaptcha():
    try:
        # Capatcha vom URLResolver verarbeiten lassen
        from urlresolver.plugins.lib import recaptcha_v2
        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(_getSiteKey(), lang='de')
        return token
    except ImportError:
        pass

def _getSiteKey():
    # Leave-Link aufrufen
    sHtmlContent = _getRequestHandler(URL_MAIN, True).request()

    # Basis-JS ermitteln
    pattern = '<script [^>]*src="([^"]*basic.min.js[^"]*)"[^>]*></script[>].*?'
    aResult = cParser().parse(sHtmlContent, pattern)

    # Falls JS gefunden => Site-Key auslesen
    if aResult[0]:
        # JS ermitteln
        sHtmlContent = _getRequestHandler(aResult[1][0], True).request()

        # Site-Key aus JS ermitteln
        pattern = "'sitekey':'(.*?)'"
        aResult = cParser().parse(sHtmlContent, pattern)

        # Site-Key gefunden? => Rückgabe
        if aResult[0]:
            return aResult[1][0]
        else:
            logger.error("error while getting sitekey: sitekey not found in basic.min.js")
    else:
        logger.error("error while getting sitekey: basic.min.js not found")

def _getRequestHandler(sUrl, bCache = False):
    # RequestHandler ohne Caching und mit User-Agent vom Firefox
    oRequest = cRequestHandler(sUrl, caching = bCache)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0')

    # Handle zurück geben
    return oRequest
