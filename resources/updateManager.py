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

## Remote path to download plugin.zip and version file.
REMOTE_PATH = "https://github.com/sraedler/plugin.video.xstream/archive/master.zip"

## Full path of the remote file version.
REMOTE_VERSION_FILE = "https://raw.githubusercontent.com/sraedler/plugin.video.xstream/master/addon.xml"

## Full path of the local file version.
LOCAL_VERSION_FILE = os.path.join(ROOT_DIR, "addon.xml")

## Full path to the local .zip file. It includes the file name.
LOCAL_FILE = os.path.join(TEMP_DIR, "xstream_update.zip")


def checkforupdates():
    logger.info("Xstream checkforupdates")

    remoteVersionXML = urllib.urlopen(REMOTE_VERSION_FILE).read()
    remoteTag = remoteVersionXML.split("updateTag=\"")[1].split("\"\n\tprovider")[0]

    localVersionXML = open(LOCAL_VERSION_FILE).read()
    localTag = localVersionXML.split("updateTag=\"")[1].split("\"\n\tprovider")[0]

    if (int(remoteTag) > int(localTag)):
        print "New Version Available"
        urllib.urlretrieve(REMOTE_PATH, LOCAL_FILE)

        updateFile = zipfile.ZipFile(LOCAL_FILE)

        for n in updateFile.namelist():
            if n[-1] != "/":
                dest = os.path.join(ADDON_DIR, n)
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                f = open(dest, 'w')
                print n
                f.write(data)
                f.close()
        updateFile.close()
        print "Update Successful"