#!/usr/bin/env python
# encoding: utf-8

from workin.extensions import BaseDiscover

from . import settings as config


class Discover(BaseDiscover):

    def execute(self, application):
        application.settings.configure(config)
