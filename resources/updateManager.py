import urllib
import os
import zipfile
import logger
import xbmc
from resources.lib import common

## Installation path.
ROOT_DIR = common.addonPath
TEMP_DIR = os.path.join(ROOT_DIR, "TEMP")
ADDON_DIR = "\\".join(ROOT_DIR.split("\\")[:-1])
XSTREAM_DIRNAME = os.path.abspath(os.path.join(ROOT_DIR, os.pardir))

## Remote path to download plugin.zip and version file.
REMOTE_PATH = "https://github.com/sraedler/plugin.video.xstream/archive/master.zip"

## Full path of the remote file version.
REMOTE_VERSION_FILE = "https://raw.githubusercontent.com/sraedler/plugin.video.xstream/master/addon.xml"

## Full path of the local file version.
LOCAL_VERSION_FILE = os.path.join(ROOT_DIR, "addon.xml")

## Full path to the local .zip file. It includes the file name.
LOCAL_FILE = os.path.join(TEMP_DIR, "xstream_update.zip")


def checkforupdates():
    logger.info("xStream checkforupdates")

    remoteVersionXML = urllib.urlopen(REMOTE_VERSION_FILE).read()
    remoteTag = remoteVersionXML.split("name=\"xStream\"\n\tversion=\"")[1].split("\"\n\tprovider")[0].translate(None, '.')

    localVersionXML = open(LOCAL_VERSION_FILE).read()
    localTag = localVersionXML.split("name=\"xStream\"\n\tversion=\"")[1].split("\"\n\tprovider")[0].translate(None, '.')

    if (int(remoteTag) > int(localTag)):
        logger.info("New Version Available")
        urllib.urlretrieve(REMOTE_PATH, LOCAL_FILE)

        updateFile = zipfile.ZipFile(LOCAL_FILE)

        for n in updateFile.namelist():
            if n[-1] != "/":
                dest = os.path.join(ADDON_DIR, XSTREAM_DIRNAME + "/" + "/".join(n.split("/")[1:]))
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                f = open(dest, 'w')
                f.write(data)
                f.close()
        updateFile.close()
        logger.info("Update Successful")