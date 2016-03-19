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

## Full path to the local .zip file. It includes the file name.
LOCAL_FILE = os.path.join(TEMP_DIR, "xStream_update.zip")


def checkforupdates():
    logger.info("xStream checkforupdates")

    REMOTE_PATH = REMOTE_PATH_BETA if (cConfig().getSetting('UpdateSetting') == "BETA") else REMOTE_PATH_MASTER
    REMOTE_VERSION_FILE = REMOTE_VERSION_FILE_BETA if (cConfig().getSetting('UpdateSetting') == "BETA") else REMOTE_VERSION_FILE_MASTER

    logger.info("Remote Path: " + REMOTE_PATH)

    remoteVersionXML = urllib.urlopen(REMOTE_VERSION_FILE).read()
    remoteVersion = ET.fromstring(remoteVersionXML).attrib['version']

    logger.info("Old Version: " + common.addon.getAddonInfo('version'))
    logger.info("New Version: " + remoteVersion)

    if (V(remoteVersion)>V(common.addon.getAddonInfo('version'))):
        logger.info("New Version Available")

        progressDialog = "Update xStream auf Version: " + ("Beta" if (cConfig().getSetting('useBeta') == "true") else "Master")
        progress = xbmcgui.DialogProgressBG()
        progress.create(progressDialog)

        if not os.path.exists(LOCAL_FILE):
            os.mkdir(TEMP_DIR)

        urllib.urlretrieve(REMOTE_PATH, LOCAL_FILE)

        updateFile = zipfile.ZipFile(LOCAL_FILE)

        for index, n in enumerate(updateFile.namelist()):
            percentage = index * 100 / len(updateFile.namelist())
            if n[-1] != "/":
                dest = os.path.join(ROOT_DIR, "/".join(n.split("/")[1:]))
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                if os._exists(dest):
                    os.remove(dest)
                f = open(dest, 'w')
                f.write(data)
                f.close()
            progress.update(percentage, progressDialog)
        updateFile.close()
        logger.info("Update Successful")
        progress.close()
