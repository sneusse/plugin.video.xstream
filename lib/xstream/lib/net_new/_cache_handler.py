# -*- coding: utf-8 -*-
import gzip
import re
import urllib2
from urllib import addinfourl
from StringIO import StringIO
from xstream.lib.database import Database

from _response import xResponse


class CacheHandler(urllib2.BaseHandler):
    def __init__(self):
        self._db = Database()

    def default_open(self, request):
        if request.get_method() == "GET":
            response = self._db.select_response(unicode(request.get_full_url()))
            if not response:
                return None

            return xResponse(response['url'], response['code'], response['msg'], response['hdrs'], response['body'])
        return None

    def http_response(self, request, response):
        if request.get_method() == "GET":
            if response.code in [301]:
                return response

            url = unicode(request.get_full_url())
            code = unicode(response.code)
            msg = unicode(response.msg)
            header = unicode(response.info())
            body = self._encode_body(response.info(), response.read())
            self._db.insert_response(url, code, msg, header, body)
        return response

    def _encode_body(self, hdrs, body):
        try:
            if hdrs['content-encoding'].lower() == 'gzip':
                body = gzip.GzipFile(fileobj=StringIO(body)).read()
        except:
            pass

        try:
            content_type = hdrs['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', body, re.IGNORECASE)
        if r:
            encoding = r.group(1)

        try:
            body = unicode(body, encoding)
        except:
            pass

        return body

    https_response = http_response


class CachedResponse(addinfourl):
    def __init__(self, url, code, msg, hdrs, body):
        self._msg = msg
        fp = StringIO(body)
        addinfourl.__init__(self, fp, hdrs, url, code)

    @property
    def msg(self):
        return self._msg