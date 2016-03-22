import urllib
import os
import xml.etree.ElementTree as ET
import zipfile
import logger
import xbmc
import xbmcgui
from resources.lib.config import cConfig
from distutils.version import LooseVersion as V
from resources.lib import common
from resources.lib import download

## Installation path.
ROOT_DIR = common.addonPath
TEMP_DIR = os.path.join(ROOT_DIR, "TEMP")
XSTREAM_DIRNAME = os.path.basename(ROOT_DIR)

## Remote path to download plugin.zip and version file.
REMOTE_PATH_BETA = "https://github.com/StoneOffStones/plugin.video.xstream/archive/beta.zip"
REMOTE_PATH_MASTER = "https://github.com/Lynx187/plugin.video.xstream/archive/master.zip"

## Full path of the remote file version.
REMOTE_VERSION_FILE_BETA = "https://raw.githubusercontent.com/StoneOffStones/plugin.video.xstream/beta/addon.xml"
REMOTE_VERSION_FILE_MASTER = "https://raw.githubusercontent.com/Lynx187/plugin.video.xstream/master/addon.xml"

## Filename of the update File.
LOCAL_FILE_NAME = "xStream_update.zip"


def checkforupdates():
    logger.info("xStream checkforupdates")

    REMOTE_PATH = REMOTE_PATH_BETA if (cConfig().getSetting('UpdateSetting') == "Beta") else REMOTE_PATH_MASTER
    REMOTE_VERSION_FILE = REMOTE_VERSION_FILE_BETA if (cConfig().getSetting('UpdateSetting') == "Beta") else REMOTE_VERSION_FILE_MASTER

    logger.info("Remote Path: " + REMOTE_PATH)

    remoteVersionXML = urllib.urlopen(REMOTE_VERSION_FILE).read()
    remoteVersion = ET.fromstring(remoteVersionXML).attrib['version']

    localVersionXML = open(os.path.join(ROOT_DIR, "addon.xml")).read()
    localVersion = ET.fromstring(localVersionXML).attrib['version']

    logger.info("Old Version: " + common.addon.getAddonInfo('version'))
    logger.info("New Version: " + remoteVersion)

    if (V(remoteVersion)>V(localVersion)):
        logger.info("New Version Available")

        download.cDownload().download(REMOTE_PATH, LOCAL_FILE_NAME, False)

        updateFile = zipfile.ZipFile(os.path.join(TEMP_DIR, LOCAL_FILE_NAME))

        for index, n in enumerate(updateFile.namelist()):
            if n[-1] != "/":
                dest = os.path.join(ROOT_DIR, "/".join(n.split("/")[1:]))
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                if os.path.exists(dest):
                    os.remove(dest)
                f = open(dest, 'w')
                f.write(data)
                f.close()
        updateFile.close()
        logger.info("Update Successful")
