# -*- coding: utf-8 -*-
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib import logger
from resources.lib import updateManager
import xbmc
import xbmcgui
import sys

# Main starting function
def run():
    parseUrl()

def changeWatched(params):
    if not cConfig().getSetting('metahandler')=='true': return
    #videoType, name, imdbID, season=season, episode=episode, year=year, watched=watched
    try:
        from metahandler import metahandlers
        meta = metahandlers.MetaData()
        season = ''
        episode = ''
        mediaType = params.getValue('mediaType')
        imdbID = params.getValue('imdbID')
        name = params.getValue('title')
        if params.exist('season'):
            season = params.getValue('season')
        if params.exist('episode'):
            episode = params.getValue('episode')
        if imdbID:
            meta.change_watched(mediaType, name, imdbID, season=season, episode=episode)
            xbmc.executebuiltin("XBMC.Container.Refresh")
    except Exception as e:
        META = False
        logger.info("Could not import package 'metahandler'")
        logger.info(e)
    return


def updateMeta(params):
    if not cConfig().getSetting('metahandler')=='true':
        return
    #videoType, name, imdbID, season=season, episode=episode, year=year, watched=watched
    try:
        from metahandler import metahandlers
    except Exception as e:
        logger.info("Could not import package 'metahandler'")
        logger.info(e)
        return
    meta = metahandlers.MetaData()
    season = ''
    episode = ''
    mediaType = params.getValue('mediaType')
    imdbID = params.getValue('imdbID')
    name = str(params.getValue('title'))
    year = params.getValue('year')
    logger.info("MediaType: "+mediaType)
    if mediaType == 'movie' or mediaType == 'tvshow':
        # show meta search input
        oGui = cGui()
        sSearchText = oGui.showKeyBoard(name)
        if not sSearchText: return
        if mediaType == 'movie':
            try:
                foundInfo = meta.search_movies(sSearchText)
            except:
                logger.info('error or nothing found')
                foundInfo = False
        elif mediaType == 'tvshow':
            foundInfo = metahandlers.TheTVDB().get_matching_shows(sSearchText, language="all", want_raw=True)
        else:
            return

        if not foundInfo:
            oGui.showInfo('xStream', 'Suchanfrage lieferte kein Ergebnis')
            return
        # select possible match
        dialog = xbmcgui.Dialog()
        items = []
        for item in foundInfo:
            if mediaType == 'movie':
                items.append(str(item['title'].encode('utf-8'))+' ('+str(item['year'])+')')
            elif mediaType == 'tvshow':
                if 'FirstAired' in item:
                    items.append(item['SeriesName']+' ('+str(item['FirstAired'])[:4]+') ' + item.get('language',''))
                else:
                    items.append(item['SeriesName']+' '+item.get('language',''))
            else:
                return
        index = dialog.select('Film/Serie wählen', items)
        if index > -1:
            item = foundInfo[index]
        else:
            return False

    if not imdbID:
        imdbID = ''
    if not year:
        year = ''
    if mediaType == 'movie':
        meta.update_meta(mediaType, name, imdbID, new_imdb_id=str(item['imdb_id']), new_tmdb_id=str(item['tmdb_id']), year=year)
    elif mediaType == 'tvshow':
        if params.exist('season'):
            season = params.getValue('season')
            meta.update_season(name, imdbID, season)
        if params.exist('episode'):
            episode = params.getValue('episode')
        if season and episode:
            meta.update_episode_meta(name, imdbID, season, episode)
        elif season:
            meta.update_season(name, imdbID, season)
        else:
            meta.update_meta(mediaType, name, imdbID, new_imdb_id=str(item.get('IMDB_ID','')), new_tmdb_id=str(item['id']), year=year)
    xbmc.executebuiltin("XBMC.Container.Refresh")
    return

def parseUrl():
    params = ParameterHandler()

    # If no function is set, we set it to the default "load" function
    if params.exist('function'):
        sFunction = params.getValue('function')
        if sFunction == 'spacer':
            return True
        elif sFunction == 'clearCache':
            from resources.lib.handler.requestHandler import cRequestHandler
            cRequestHandler('dummy').clearCache()
            return
        elif sFunction == 'changeWatched':
            changeWatched(params)
            return
        elif sFunction == 'updateMeta':
            updateMeta(params)
            return
        elif sFunction == 'searchAlter':
            searchAlter(params)
            return
        elif sFunction == 'updateXstream' and cConfig().getSetting('UpdateSetting') != 'Off':
            updateManager.checkforupdates()
            return
    else:
      sFunction = 'load'

    # Test if we should run a function on a special site
    if not params.exist('site'):
        xbmc.executebuiltin('XBMC.RunPlugin(%s?function=clearCache)' % sys.argv[0])
        xbmc.executebuiltin('XBMC.RunPlugin(%s?function=updateXstream)' % sys.argv[0])
        # As a default if no site was specified, we run the default starting gui with all plugins
        showMainMenu(sFunction)
        return
    sSiteName = params.getValue('site')
    logger.info (params.getAllParameters())
    if params.exist('playMode'):
        from resources.lib.gui.hoster import cHosterGui
        url = False
        playMode = params.getValue('playMode')
        isHoster = params.getValue('isHoster')
        url = params.getValue('url')
        manual = params.exist('manual')
        if cConfig().getSetting('hosterSelect')=='auto' and playMode != 'jd' and playMode != 'pyload' and not manual:
            cHosterGui().streamAuto(playMode, sSiteName, sFunction)
        else:
            cHosterGui().stream(playMode, sSiteName, sFunction, url)
        return
    logger.info("Call function '%s' from '%s'" % (sFunction, sSiteName))
    # If the hoster gui is called, run the function on it and return
    if sSiteName == 'cHosterGui':
        showHosterGui(sFunction)
    # If global search is called
    elif sSiteName == 'globalSearch':
        searchGlobal()
    elif sSiteName == 'favGui':
        showFavGui(sFunction)
    # If addon settings are called
    elif sSiteName == 'xStream':
        oGui = cGui()
        oGui.openSettings()
        oGui.updateDirectory()
    # If the urlresolver settings are called
    elif sSiteName == 'urlresolver':
        import urlresolver
        urlresolver.display_settings()
    # If metahandler settings are called
    elif sSiteName == 'metahandler':
        import metahandler
        metahandler.display_settings()
    else:
        # Else load any other site as plugin and run the function
        plugin = __import__(sSiteName, globals(), locals())
        function = getattr(plugin, sFunction)
        function()

def showMainMenu(sFunction):
    oGui = cGui()
    oPluginHandler = cPluginHandler()
    aPlugins = oPluginHandler.getAvailablePlugins()
    if not aPlugins:
        logger.info("No Plugins found")
        # Open the settings dialog to choose a plugin that could be enabled
        oGui.openSettings()
        oGui.updateDirectory()
    else:
        # Create a gui element for every plugin found
        for aPlugin in aPlugins:
            oGuiElement = cGuiElement()
            oGuiElement.setTitle(aPlugin['name'])
            oGuiElement.setSiteName(aPlugin['id'])
            oGuiElement.setFunction(sFunction)
            if 'icon' in aPlugin and aPlugin['icon']:
                oGuiElement.setThumbnail(aPlugin['icon'])
            oGui.addFolder(oGuiElement)

        # Create a gui element for global search
        oGuiElement = cGuiElement()
        oGuiElement.setTitle("Globale Suche")
        oGuiElement.setSiteName("globalSearch")
        oGuiElement.setFunction("globalSearch")
        #oGuiElement.setThumbnail("DefaultAddonService.png")
        oGui.addFolder(oGuiElement)

        # Create a gui element for favorites
        #oGuiElement = cGuiElement()
        #oGuiElement.setTitle("Favorites")
        #oGuiElement.setSiteName("FavGui")
        #oGuiElement.setFunction("showFavs")
        #oGuiElement.setThumbnail("DefaultAddonService.png")
        #oGui.addFolder(oGuiElement)

        # Create a gui element for addon settings
        oGuiElement = cGuiElement()
        oGuiElement.setTitle("xStream Settings")
        oGuiElement.setSiteName("xStream")
        oGuiElement.setFunction("display_settings")
        oGuiElement.setThumbnail("DefaultAddonService.png")
        oGui.addFolder(oGuiElement)

        # Create a gui element for urlresolver settings
        oGuiElement = cGuiElement()
        oGuiElement.setTitle("Resolver Settings")
        oGuiElement.setSiteName("urlresolver")
        oGuiElement.setFunction("display_settings")
        oGuiElement.setThumbnail("DefaultAddonService.png")
        oGui.addFolder(oGuiElement)

        # Create a gui element for metahandler settings
        if cConfig().getSetting('metahandler')=='true':
            oGuiElement = cGuiElement()
            oGuiElement.setTitle("Metahandler Settings")
            oGuiElement.setSiteName("metahandler")
            oGuiElement.setFunction("display_settings")
            oGuiElement.setThumbnail("DefaultAddonService.png")
            oGui.addFolder(oGuiElement)
    oGui.setEndOfDirectory()

def showHosterGui(sFunction):
    from resources.lib.gui.hoster import cHosterGui
    oHosterGui = cHosterGui()
    function = getattr(oHosterGui, sFunction)
    function()
    return True

#def showFavGui(functionName):
    #from resources.lib.gui.favorites import FavGui
    #oFavGui = FavGui()
    #function = getattr(oFavGui, functionName)
    #function()
    #return True

def searchGlobal():
    import threading
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return True
    aPlugins = []
    aPlugins = cPluginHandler().getAvailablePlugins()
    dialog = xbmcgui.DialogProgress()
    dialog.create('xStream',"Searching...")
    numPlugins = len(aPlugins)
    threads = []
    for count, pluginEntry in enumerate(aPlugins):
        dialog.update((count+1)*100/numPlugins,'Searching: '+str(pluginEntry['name'])+'...')
        logger.info('Searching for %s at %s' % (sSearchText, pluginEntry['id']))
        t = threading.Thread(target=_pluginSearch, args=(pluginEntry,sSearchText,oGui))
        threads += [t]
        t.start()
    for t in threads:
        t.join()
    dialog.close()
    oGui.setView()
    oGui.setEndOfDirectory()
    return True

def searchAlter(params):
    searchTitle = params.getValue('searchTitle')
    searchImdbId = params.getValue('searchImdbID')
    searchYear = params.getValue('searchYear')
    import threading
    oGui = cGui()
    aPlugins = []
    aPlugins = cPluginHandler().getAvailablePlugins()
    dialog = xbmcgui.DialogProgress()
    dialog.create('xStream',"Searching...")
    numPlugins = len(aPlugins)
    threads = []
    for count, pluginEntry in enumerate(aPlugins):
        dialog.update((count+1)*100/numPlugins,'Searching: '+str(pluginEntry['name'])+'...')
        logger.info('Searching for ' + searchTitle + pluginEntry['id'].encode('utf-8'))
        t = threading.Thread(target=_pluginSearch, args=(pluginEntry,searchTitle, oGui))
        threads += [t]
        t.start()
    for t in threads:
        t.join()
    #check results, put this to the threaded part, too
    dialog.close()
    filteredResults = []
    for result in oGui.searchResults:
        print 'Site: %s Titel: %s' % (result.getSiteName(), result.getTitle())
        if not searchTitle in result.getTitle(): continue
        if result.getYear() and result.getYear() != year: continue
        if result.getItemProperties().get('imdbID',False) and result.getItemProperties().get('imdbID',False) != searchImdbId: continue
        filteredResults.append(result)

    for result in filteredResults:
        print 'Site: %s Titel: %s' % (result.getSiteName(), result.getTitle())

    oGui.setView()
    oGui.setEndOfDirectory()
    #xbmc.executebuiltin('Container.Update')
    return True

def _pluginSearch(pluginEntry, sSearchText, oGui):
    try:
        plugin = __import__(pluginEntry['id'], globals(), locals())
        function = getattr(plugin, '_search')
        function(oGui, sSearchText)
    except:
        logger.info(pluginEntry['name']+': search failed')
        import traceback
        print traceback.format_exc()
