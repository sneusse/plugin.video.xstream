import urllib
import os
import time
import xml.etree.ElementTree as ET
import json
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
REMOTE_URL_MASTER = "https://github.com/Lynx187/plugin.video.xstream/archive/master.zip"
REMOTE_URL_BETA = "https://github.com/StoneOffStones/plugin.video.xstream/archive/beta.zip"
REMOTE_URL_NIGHTLY = "https://github.com/StoneOffStones/plugin.video.xstream/archive/nightly.zip"

## Full path of the remote file version.
REMOTE_VERSION_FILE_MASTER = "https://raw.githubusercontent.com/Lynx187/plugin.video.xstream/master/addon.xml"
REMOTE_VERSION_FILE_BETA = "https://raw.githubusercontent.com/StoneOffStones/plugin.video.xstream/beta/addon.xml"


## Filename of the update File.
LOCAL_FILE_NAME = "xStream_update.zip"
LOCAL_NIGHTLY_VERSION = os.path.join(TEMP_DIR, "nightly_commit_sha")


def checkforupdates():
    logger.info("xStream checkforupdates")

    if cConfig().getSetting('UpdateSetting') == "Nightly":
        nightlycommitsXML = urllib.urlopen("https://api.github.com/repos/StoneOffStones/plugin.video.xstream/commits/nightly").read()

        try:
            if not os.path.exists(LOCAL_NIGHTLY_VERSION) or open(LOCAL_NIGHTLY_VERSION).read() != json.loads(nightlycommitsXML)['sha']:
                    update(REMOTE_URL_NIGHTLY)
                    open(LOCAL_NIGHTLY_VERSION, 'w').write(json.loads(nightlycommitsXML)['sha'])
        except:
            logger.info("Ratelimit reached")

    elif cConfig().getSetting('UpdateSetting') == "Beta":
        if getRemoteVersion(REMOTE_VERSION_FILE_BETA) > getLocalVersion():
            update(REMOTE_URL_BETA)

    elif cConfig().getSetting('UpdateSetting') == "Stable":
        if getRemoteVersion(REMOTE_VERSION_FILE_MASTER) > getLocalVersion():
            update(REMOTE_URL_MASTER)


def getLocalVersion():
    xml = open(os.path.join(ROOT_DIR, "addon.xml")).read()
    version = V(ET.fromstring(xml).attrib['version'])
    logger.info("xStream Localversion: " + version.vstring)
    return version


def getRemoteVersion(REMOTE_VERSION_URL):
    xml = urllib.urlopen(REMOTE_VERSION_URL).read()
    version = V(ET.fromstring(xml).attrib['version'])
    logger.info("xStream Remoteversion: " + version.vstring)
    return version


def update(REMOTE_PATH):

    logger.info("xStream Update URL: " + REMOTE_PATH)

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
