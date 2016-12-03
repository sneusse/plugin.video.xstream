# coding: UTF-8

import sys

import time
import json as j
import base64 as l1
import hmac as l11ll1
import hashlib as l1ll
from xstream.lib.utils import l1111

try:
    l11l1l = l1111 (u"ࡗࡓࡔࡐࡧࡏࡦ࠳࡙ࡳࡸࡷࡍࡣࡥࡉࡈࡖ࡫ࡍࡧࡵࡻ࠴࠷࠻ࡁࡂ࠵ࡅࡹࡨࠥ")
    l1l111 = l1111 (u"࠹ࡎࡋࡳࡕࡪ࡚ࡵࡅࡍࡍࡺ࡫ࡓࡪࡺ࠻࠵ࡻࡊࡊࡩࡒࡵࡑࡼࡢࡍࡖ࠼ࡵࡔ࠳")
except:
    pass


def get_headers(string):
    return {l1111(u"ࡄࡖ࠱࡙ࡵ࡫ࡦࡰࠥ"): l111ll(string), l1111(u"ࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹࠦ"):l1111(u"ࡧࡹ࠮ࡢࡰࡧࡶࡴ࡯ࡤ࠽")}

def l111ll(l1lll):
    l11l11 = int(time.time())
    l11lll = {}
    l11lll[l1111(u"ࡱࡷࡥࡰ࡮ࡩ࡟࡬ࡧࡼࠫ")] = l11l1l
    l11lll[l1111(u"ࡸ࡮ࡳࡥࡴࡶࡤࡱࡵࡑ")] = l11l11
    l11lll[l1111(u"ࡩ࡯ࡤࡧࡇ")] = l1l11(l11l11, l1lll)
    return l1.b64encode(j.dumps(l11lll).encode(l1111(u"ࡻࡴࡧ࠯࠻ࠩ")))


def l1l11(l11l11, l1l1l):
    l1ll1 = l1l111.encode(l1111(u'ࡺࡺࡦ࠮࠺ࡒ'))
    l1l1ll = str(l11l11) + l1111(u'࠵ࠛ') + str(l1l1l)
    l1l1ll = l1l1ll.encode(l1111(u'ࡦࡹࡣࡪ࡫࠯'))
    l1lllll = l11ll1.new(l1ll1, l1l1ll, digestmod=l1ll.sha256)
    return l1lllll.hexdigest()
