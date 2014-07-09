#!/usr/bin/env python
# encoding: utf-8

"""
@Author: Alvin
@Email: yao.angellin@gmail.com
@Date: 2014-07-04 23:22:22
@Desc: workin global settings module, which will be set in tornado application.
Usage:
    from workin.conf import settings

    xxx = settings.xxx
    xxx = settings['xxx']
"""
import logging
import warnings

from workin.utils import importlib
from workin.conf import global_settings


class Settings(object):

    TUPLE_SETTINGS = ("TEMPLATE_DIRS", "INSTALLED_APPS")

    def configure(self, settings_module=None, override=False):
        self.set_module_value(global_settings)
        # Override with user custom settings.
        if settings_module:
            if isinstance(settings_module, basestring):
                try:
                    settings_module = importlib.import_module(settings_module)
                except ImportError:
                    logging.exception("Cannot import settings '%s'. (Is is in \
                            sys.path?)" % (settings_module))
            self.set_module_value(settings_module, override)

        if not self.__dict__.get('COOKIE_SECRET'):
            warnings.warn("The COOKIE_SECRET settings must not be empty.",
                    DeprecationWarning)

        return self

    def set_module_value(self, module, override=False):
        for setting in dir(module):
            value = getattr(module, setting)
            if setting in self.TUPLE_SETTINGS and isinstance(value,
                    basestring):
                value = (getattr(module, setting), )
            if override or setting.lower() not in self.__dict__:
                # tornado settings should be lowercase only.
                self.__dict__[setting.lower()] = value

    def __setattr__(self, name, value):
        self.__dict__[name.lower()] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError("Settings has no attribute `%s`" % name)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __delitem__(self, name):
        del self.__dict__[name]

    def get(self, name, default=None):
        if name in self.__dict__:
            return self.__dict__(name)
        return default

    def to_dict(self):
        return self.__dict__
