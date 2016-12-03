# -*- coding: utf-8 -*-
import os

from xstream import common


class Settings:
    _xml_data = {}
    _parent = ''
    _prefix = ''

    def _append_line(self, line):
        pass

    def _has_category(self, category):
        return category in self._xml_data

    def _create_setting(self, category='', **kwargs):
        if not category:
            if not self._parent:
                raise Exception
            else:
                category = self._parent

        if not self._has_category(category):
            raise Exception # or create???

        setting = '<setting'

        for key in kwargs:
            if kwargs[key] is not '':
                if key == 'id' and self._prefix:
                    setting = setting + ' %s="%s_%s"' % (key, self._prefix, kwargs[key])
                else:
                    setting = setting + ' %s="%s"' % (key, kwargs[key])

        setting = setting + ' />'

        self._xml_data[category].append(setting)

    def get_parent(self):
        return self._parent

    def set_parent(self, category):
        if self._has_category(category):
            self._parent = category
        else:
            raise

    def get_prefix(self):
        return self._prefix

    def set_prefix(self, prefix):
        self._prefix = prefix

    def clear_prefix(self):
        self._prefix = ''

    def create_category(self, label):
        if self._has_category(label):
            return
        self._xml_data[label] = []
        self._parent = label

    def create_sep(self, category=''):
        """
        Shows a horizontal line

        :param category:
        :return:
        """
        self._create_setting(category, type='sep')

    def create_lsep(self, label, category=''):
        """
        Shows a horizontal line with a text

        :param label: an id from the language file that indicates which text to display
        :param category:
        :return:
        """
        self._create_setting(category, type='lsep', label=label)

    def create_input_text(self, id, label, option='', default='', category='', enable=''):
        """
        Allow a user to enter one line of text.

        :param id: the name of the setting
        :param label: an id from the language file that indicates which text to display
        :param option: "hidden" or "urlencoded"
        :param default: the default value
        :param category:
        :return:
        """
        self._create_setting(category, type='text', id=id, label=label, option=option, default=default, enable=enable)

    def create_input_ipaddress(self, id, label, default='', category=''):
        pass

    def create_input_number(self, id, label, default='', category=''):
        pass

    def create_input_slider(self, id, label, min, max, step=1, option='', default='', category=''):
        pass

    def create_input_date(self, id, label, default='', category=''):
        pass

    def create_input_time(self, id, label, default='', category=''):
        pass

    def create_input_bool(self, id, label, default='', category='', enable=''):
        self._create_setting(category, type='bool', id=id, label=label, default=default, enable=enable)

    def create_select(self, id, label, values, category=''):
        pass

    def create_action(self, label, action, category=''):
        pass

    def generate_xml(self):
        try:
            os.makedirs(os.path.dirname(common.settings_file))
        except OSError:
            pass

        xml = [
            '<?xml version="1.0" encoding="utf-8" standalone="yes"?>',
            '<settings>'
        ]

        for cat in self._xml_data:
            xml.append('\t<category label="%s">' % cat)
            for setting in self._xml_data[cat]:
                xml.append('\t\t%s' % setting)
            xml.append('\t</category>')

        xml.append('</settings>')
        xml = '\n'.join(xml)

        try:
            with open(common.settings_file, 'w') as f:
                f.write(xml)
        except:
            raise