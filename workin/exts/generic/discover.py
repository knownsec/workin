#!/usr/bin/env python
# encoding: utf-8

from workin.extensions import BaseDiscover

from .urls import ADMIN_HANDLERS


class Discover(BaseDiscover):

    def execute(self, application):
        __import__('pdb').set_trace()
        application.handlers.extend(ADMIN_HANDLERS)
        application.settings['installed_apps'] += 'workin.exts.admin'
