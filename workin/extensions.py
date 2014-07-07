#!/usr/bin/env python
# encoding: utf-8

import logging
from workin.utils import importlib


def find_extensions(ext_module):

    try:
        ext_class = importlib.import_module(ext_module + '.discover')
    except ImportError, e:
        logging.exception("Error found while discovering workin \
                extension '%s': %s" % (ext_module, e))

    return ext_class.Discover()


class BaseDiscover(object):

    def execute(self, **kwargs):
        raise NotImplementedError
