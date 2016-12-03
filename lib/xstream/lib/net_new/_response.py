# -*- coding: utf-8 -*-
import StringIO

from urllib import addinfourl


class xResponse(addinfourl):
    def __init__(self, url, code, msg, hdrs, body):
        self._msg = msg
        fp = StringIO.StringIO(body)
        addinfourl.__init__(self, fp, hdrs, url, code)

    @property
    def msg(self):
        return self._msg
