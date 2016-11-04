# -*- coding: utf-8 -*-
import urllib2, re
from binascii import unhexlify
from binascii import hexlify
from resources.lib import pyaes
from resources.lib import logger
from resources.lib.parser import cParser

class cBFScrape:

    COOKIE_NAME = 'BLAZINGFAST-WEB-PROTECT'

    @staticmethod
    def checkBFCookie(content):
        '''
        returns True if there seems to be a protection 
        '''
        return COOKIE_NAME in content

    #not very robust but lazieness...
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def unprotect(initialRequest):
        content = initialRequest.request()
        if 'Blazingfast.io' not in content:
            return content
        pattern = 'xhr\.open\("GET","([^,]+),'
        match = cParser.parse(content,pattern)
        if not match[0]:
            return False
        urlParts = match[1][0].split('"')
        sid = '1200'
        url = '%s%s%s%s' % (URL_MAIN[:-1], urlParts[0],sid,urlParts[2])
        request = cRequestHandler(url,caching = False)
        request.addHeaderEntry('Referer',initialRequest.getRequestUri())
        content = request.request()
        if not blazingfast.checkBFCookie(content):
            return content #even if its false its probably not the right content, we'll see
        cookie = blazingfast.getCookieString(content)
        if not cookie: 
            return False
        initialRequest.caching = False
        name, value = cookie.split(';')[0].split('=')
        cookieData = dict((k.strip(), v.strip()) for k,v in (item.split("=") for item in cookie.split(";")))     
        cookie = initialRequest.createCookie(name,value,domain=cookieData['domain'], expires=sys.maxint, discard=False)
        initialRequest.setCookie(cookie)
        content = initialRequest.request()
        return content