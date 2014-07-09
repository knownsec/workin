#!/usr/bin/env python
# encoding: utf-8

import os
from tornado.web import url, StaticFileHandler

from .handlers import (AdminDashboardHandler, AdminListHandler,
        AdminEditHandler, AdminAddHandler, AdminDetailHandler)

ADMIN_STATIC_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'static/')

ADMIN_HANDLERS = (
    url(r'/admin/static/(.*)', StaticFileHandler, {'path':
        ADMIN_STATIC_PATH}, name='admin-static-url'),
    url(r'/admin/', AdminDashboardHandler, name='admin-dashboard'),
    url(r'/admin/list/(?P<model>[^\/]+)/(?P<page>\d+)/', AdminListHandler,
        name='admin-list'),
    url(r'/admin/edit/(?P<model>[^\/]+)/(?P<id>\d+)/', AdminEditHandler,
        name='admin-edit'),
    url(r'/admin/add/(?P<model>[^\/]+)/', AdminAddHandler, name='admin-add'),
    url(r'/admin/detail/(?P<model>[^\/]+)/(?P<id>\d+)/', AdminDetailHandler,
        name='admin-detail')
)
