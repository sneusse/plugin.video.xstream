# -*- coding: utf-8 -*-
import urllib2, re
from binascii import unhexlify
from binascii import hexlify
from resources.lib import pyaes
from resources.lib import logger

COOKIE_NAME = 'BLAZINGFAST-WEB-PROTECT'

def check(content):
    '''
    returns True if there seems to be a protection 
    '''
    return COOKIE_NAME in content

#not very robust but lazieness...
def getCookieString(content):
    vars = re.findall('toNumbers\("([^"]+)"',content)
    if not vars:
        logger.info('vars not found')
        return False
    value = _decrypt(vars[2], vars[0], vars[1])
    if not value:
        logger.info('value decryption failed')
        return False
    pattern = '"%s=".*?";([^"]+)"' % COOKIE_NAME
    cookieMeta = re.findall(pattern,content)
    if not cookieMeta:
        logger.info('cookie meta not found')
    cookie = "%s=%s;%s" % (COOKIE_NAME, value, cookieMeta[0])
    return cookie
    # + toHex(BFCrypt.decrypt(c, 2, a, b)) +

def _decrypt(msg, key, iv):
    msg = unhexlify(msg)
    key = unhexlify(key)
    iv = unhexlify(iv)
    if len(iv) != 16:
        logger.info("iv length is" + str(len(iv)) +" must be 16.")
        return False
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
    plain_text = decrypter.feed(msg)
    plain_text += decrypter.feed()
    f = hexlify(plain_text)
    return f 