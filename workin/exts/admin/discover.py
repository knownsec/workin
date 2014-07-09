#!/usr/bin/env python
# encoding: utf-8
import logging

from workin.conf import settings
from workin.extensions import BaseDiscover
from workin.utils import importlib

from .urls import ADMIN_HANDLERS
from . import settings as config


class Discover(BaseDiscover):

    def execute(self, application):
        settings.configure(config)
        application.settings = settings.to_dict()

        application.settings['installed_apps'] += ('workin.exts.admin',)
        logging.debug("Add 'workin.exts.admin' to INSTALLED_APPS.")

        application.handlers.extend(ADMIN_HANDLERS)
        logging.debug("Add admin handlers for extension 'workin.exts.admin'.")

        for app in application.settings['installed_apps']:
            try:
                importlib.import_module(app + '.admin')
            except ImportError:
                # No admin.py for the specified app
                pass
