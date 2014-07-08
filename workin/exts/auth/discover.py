#!/usr/bin/env python
# encoding: utf-8

from workin.extensions import BaseDiscover
from workin.conf import settings

from . import settings as config


class Discover(BaseDiscover):

    def execute(self, application):
        settings.configure(config)
        application.settings = settings.to_dict()
        application.settings['installed_apps'] += ('workin.exts.auth',)
