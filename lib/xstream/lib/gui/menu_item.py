# -*- coding: utf-8 -*-
import json
from xstream.lib import utils


class MenuItem(object):
    def __init__(self, title, mode):
        self._title = title
        self._mode = mode

    @property
    def title(self):
        return self._title

    @property
    def mode(self):
        return self._mode

    def get_dict(self):
        return {'mode':self.mode}


class PluginMenuItem(MenuItem):
    def __init__(self, title, func, info_item=None, params=None, id=None):
        super(PluginMenuItem, self).__init__(title, 'plugin')

        self._id = id
        self._func = func
        self._info_item = info_item
        self._params = params

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not self._id:
            self._id = value

    @property
    def func(self):
        return self._func

    @property
    def info_item(self):
        return self._info_item

    @property
    def params(self):
        return self._params

    def get_dict(self):
        base_dict = MenuItem.get_dict(self)
        self_dict = {'plugin_id': self.id, 'plugin_func': self.func}

        if self.params:
            self_dict['plugin_params'] = json.dumps(self.params)

        return utils.merge_dicts(base_dict, self_dict)

    def __repr__(self):
        return "<PluginMenuItem['id':'%s', 'func':'%s', 'params':'%s'],>" % (self.id, self.func, self.params)
