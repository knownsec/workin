#!/usr/bin/env python
# encoding: utf-8
import logging

from tornado.web import url, StaticFileHandler

from workin.conf import settings
from workin.extensions import BaseDiscover
from workin.utils import importlib

from . import settings as config
from .handlers import (AdminDashboardHandler, AdminListHandler,
        AdminEditHandler, AdminAddHandler, AdminDetailHandler)


class Discover(BaseDiscover):

    def execute(self, application):
        settings.configure(config)
        application.settings = settings.to_dict()

        application.settings['installed_apps'] += ('workin.exts.admin',)
        logging.debug("Add 'workin.exts.admin' to INSTALLED_APPS.")

        application.settings['template_dirs'] += (config.ADMIN_TEMPLATE_PATH, )

        ADMIN_HANDLERS = (
            url(r'/admin/static/(.*)', StaticFileHandler, {'path':
                application.settings['admin_static_path']},
                name='admin-static-url'),
            url(r'/admin/list/(?P<model>[^\/]+)/(?P<page>\d+)/', AdminListHandler,
                name='admin-list'),
            url(r'/admin/edit/(?P<model>[^\/]+)/(?P<id>\d+)/', AdminEditHandler,
                name='admin-edit'),
            url(r'/admin/add/(?P<model>[^\/]+)/', AdminAddHandler, name='admin-add'),
            url(r'/admin/detail/(?P<model>[^\/]+)/(?P<id>\d+)/',
                AdminDetailHandler, name='admin-detail'),
            url(r'/admin/', AdminDashboardHandler, name='admin-dashboard'),
        )

        application.handlers.extend(ADMIN_HANDLERS)
        logging.debug("Add admin handlers for extension 'workin.exts.admin'.")

        for app in application.settings['installed_apps']:
            try:
                importlib.import_module(app + '.admin')
            except ImportError:
                # No admin.py for the specified app
                pass
