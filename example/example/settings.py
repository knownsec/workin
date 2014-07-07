#!/usr/bin/env python
# coding: utf-8

DEBUG = True

INSTALLED_APPS = ('example.apps.accounts',)

SQLALCHEMY_ENGINE_URL = 'sqlite:///sqlite.db'

WORKIN_EXTENSIONS = ('workin.exts.auth',)

SESSION_SECRET = 'lfdsajfiodsajflewjfqweajkdlsajfljal'
SESSION_OPTIONS = {
        'redis_host': '127.0.0.1',
        'redis_port': 6379,
        }
SESSION_TIMEOUT = 60

try:
    from local_settings import *
except ImportError:
    pass
