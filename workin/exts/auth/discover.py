#!/usr/bin/env python
# encoding: utf-8

from workin.conf import settings
from workin.extensions import BaseDiscover

from . import settings as config

# explicitly imported to add tables
# before Base.metadata.create_all
from . import models


class Discover(BaseDiscover):

    def execute(self, application):
        settings.configure(config)
