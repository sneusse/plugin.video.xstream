from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler

SITE_IDENTIFIER = 'video4k_to'
SITE_NAME = 'Video4k'
SITE_ICON = 'video4k.png'

URL_REQUEST = 'http://video4k.to/request'

DEFAULT_REQUEST_PARAMS = dict(sEcho=1, iColumns=1, sColumns="", iDisplayStart=0, iDisplayLength=50, mDataProp_0=0,
                              mDataProp_1=1, mDataProp_2=2, mDataProp_3=3, mDataProp_4=4, sSearch="", bRegex="false",
                              sSearch_0="", bRegex_0="false", bSearchable_0="true", sSearch_1="", bRegex_1="false",
                              bSearchable_1="true", sSearch_2=" ", bRegex_2="false", bSearchable_2="true",
                              sSearch_3="", bRegex_3="false", bSearchable_3="true", sSearch_4="", bRegex_4="false",
                              bSearchable_4="true", iSortCol_0="0", sSortDir_0="asc", iSortingCols=1,
                              bSortable_0="false", bSortable_1="true", bSortable_2="false", bSortable_3="false",
                              bSortable_4="true", type="movies", filter="")

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()

    params.setParam('type', 'movies')
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('type', 'cinema')
    oGui.addFolder(cGuiElement('Kino Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('type', 'series')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showEntries(sGui = False, sSearchText = None):
    oGui = sGui if sGui else cGui()
    oParams = ParameterHandler()

    oRequest = cRequestHandler(URL_REQUEST)
    for key in DEFAULT_REQUEST_PARAMS:
        oRequest.addParameters(key, DEFAULT_REQUEST_PARAMS[key])
    oRequest.addParameters('type', oParams.getValue('type'))
    if sSearchText:
        oRequest.addParameters('sSearch', sSearchText)
        oRequest.addParameters('type', '')
    oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()

    isMatch, aResult = cParser().parse(sHtmlContent, '#tt(\d*).*?">(.*?)<')

    if not isMatch:
        if not sGui: oGui.showInfo('xStream','Es wurde kein Eintrag gefunden')
        return

    for id, sName in aResult:
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oParams.setParam('id', id)
        oGui.addFolder(oGuiElement, oParams, False, isHoster=True)

    oGui.setEndOfDirectory()


def showHosters():
    oParams = ParameterHandler()
    oRequest = cRequestHandler(URL_REQUEST)

    oRequest.addParameters('mID', oParams.getValue('id'))
    oRequest.addParameters('raw', 'true')
    oRequest.addParameters('language', 'en')

    sHtmlContent = oRequest.request()
    isMatch, aResult = cParser().parse(sHtmlContent, 'name":"(.*?)".*?URL":"(.*?)"')

    hosters = []
    if not isMatch:
        return hosters

    for sName, sUrl in aResult:
        hoster = dict()
        hoster['link'] = sUrl.replace('\\', '')
        hoster['name'] = sName
        hosters.append(hoster)

    if hosters:
        hosters.append('getHosterUrl')

    return hosters

def getHosterUrl(sUrl=False):
    if not sUrl: sUrl = ParameterHandler().getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()

def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(oGui, sSearchText)