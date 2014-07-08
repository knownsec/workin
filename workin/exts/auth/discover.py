#!/usr/bin/env python
# encoding: utf-8

from workin.conf import settings
from workin.extensions import BaseDiscover

from . import settings as config


class Discover(BaseDiscover):

    def execute(self, application):
        settings.configure(config)
        # application.handlers.extend([
        #     (r'/', auth.Index),
        #     (r'/admin', auth.Admin),
        #     (r'/register', auth.Register),
        #     (r'/login', auth.Login),
        #     (r'/logout', auth.Logout),
        # ])
