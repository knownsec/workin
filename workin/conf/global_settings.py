#!/usr/bin/env python
# encoding: utf-8

import base64
import os

DEBUG = True

LOGIN_URL = '/login/'

XSRF_COOKIES = True

# Secret key for cookies and password salt generation.
COOKIE_SECRET = base64.b64encode(os.urandom(32))
CSRF_COOKIE_NAME = "csrftoken"

STATIC_PATH = 'static'

TEMPLATE_PATH = 'templates/'

CACHE_DIRECTORY = '/tmp'

AUTOESCAPE = False

WORKIN_EXTENSIONS = []

INSTALLED_APPS = []

# Session engine settings
SESSION_ENGINE = 'workin.session.backends.redis_session.RedisSessionEngine'
SESSION_ENGINE_KWARGS = {}

# sqlalchemy settings
SQLALCHEMY_ENGINE_URL = None
SQLALCHEMY_ENGINE_KWARGS = {}

# Jinja2 settings
JINJA2_TEMPLATE_DIRS = []
JINJA2_SETTINGS = {"cache_size": 100}
JINJA2_CONTEXT_PROCESSORS = []

# Low level tornado options.
TORNADO_TRANSFORMS = None
TORNADO_DEFAULT_HOST = ""
TORNADO_WSGI_MODE = False
TORNADO_SETTINGS = {}
