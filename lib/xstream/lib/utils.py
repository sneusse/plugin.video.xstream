# -*- coding: utf-8 -*-
import sys

from xstream.lib import logger

l1lll1 = sys.version_info[0] == 2
l11 = 26
l1l1l1 = 2048
l11l = 7
l1l1 = False


def l1111(ll):
    global l1lll1
    global l11
    global l1l1l1
    global l11l

    l1ll11 = ord(ll[-1]) - l1l1l1
    ll = ll[:-1]

    if ll:
        l111l1 = (l1ll11) % len(ll)
    else:
        l111l1 = 0

    if l1lll1:
        l111 = u''.join([unichr(ord(l1111l) - l1l1l1 - (l1l11l + l1ll11) % l11l) for l1l11l, l1111l in
                         enumerate(ll[:l111l1] + ll[l111l1:])])
    else:
        l111 = ''.join([unichr(ord(l1111l) - l1l1l1 - (l1l11l + l1ll11) % l11l) for l1l11l, l1111l in
                        enumerate(ll[:l111l1] + ll[l111l1:])])

    if l1l1:
        return str(l111)
    else:
        return l111


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def get_metahandler():
    try:
        from metahandler import metahandlers
        return metahandlers.MetaData(tmdb_api_key=l1111(u"࠻࠺ࡩࡪ࠱࠹ࡤ࠳࠸࠽࠽࠴ࡥ࠻ࡦ࠽࠹ࡧࡦࡢࡦࡧࡩ࠼࠿࠹࠴ࡦ࠼࠸ࡪ࠹ࠦ"))
    except Exception as e:
        logger.info("Could not import package 'metahandler'")
        logger.info(e)
        return False