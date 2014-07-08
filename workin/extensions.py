#!/usr/bin/env python
# encoding: utf-8

import logging
from workin.utils import importlib


def find_extensions(ext_module):

    ext_class = None
    try:
        ext_class = importlib.import_module(ext_module + '.discover')
    except ImportError, e:
        logging.exception("Error found while discovering workin "
                "extension '%s': %s" % (ext_module, e))
        raise

    if ext_class and hasattr(ext_class, 'Discover'):
        return ext_class.Discover()

    return None


class BaseDiscover(object):

    def execute(self, **kwargs):
        raise NotImplementedError
