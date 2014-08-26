#!/usr/bin/env python
# encoding: utf-8

import json
import logging

import tornado.web
import tornado.options
from jinja2 import Environment, FileSystemLoader

from workin.conf import settings
from workin.middleware import MiddlewareManager
from workin.mixins.flash_message import FlashMessageMixin
from workin.mixins.jinja2 import Jinja2Mixin
from workin.session import Session
from workin.utils import importlib
from workin.routes import Route


class Application(tornado.web.Application):

    db = None
    session_engine = None
    jinja_env = None
    handlers = []
    context_processors = []

    def __init__(self, settings_module):
        settings.configure(settings_module, True)
        self.settings = settings.to_dict()
        self._setup_extensions()
        self._setup_session_engine()
        self._setup_database_engine()
        self._setup_template_loaders()
        self._setup_installed_apps()
        self._setup_context_processors()

        tornado.web.Application.__init__(self, handlers=self.handlers,
                **self.settings)

        # Due to middleware run_init_hooks will call Application, so execute
        # this at last.
        self._setup_middlewares()

    def __call__(self, request):
        try:
            self.middleware_manager.run_call_hooks(request)
            handler = tornado.web.Application.__call__(self, request)
            self.middleware_manager.run_endcall_hooks(handler)
        except Exception, e:
            logging.error(e)
            raise

    def _setup_middlewares(self):
        self.middleware_manager = MiddlewareManager(**self.settings)
        self.middleware_manager.run_init_hooks(self)

    def _setup_context_processors(self):
        # load context processors
        processors = self.settings.get('context_processors', [])
        self.context_processors = [importlib.load_class(x) for x in set(processors)]

    def _setup_database_engine(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import scoped_session, sessionmaker
        from workin.database import Base

        engine_url = self.settings['sqlalchemy_engine_url']
        engine_kwargs = self.settings['sqlalchemy_engine_kwargs']

        if not engine_url:
            return

        self.engine = create_engine(engine_url, **engine_kwargs)
        self.db = scoped_session(sessionmaker(bind=self.engine))

        Base.metadata.create_all(bind=self.engine)

    def _setup_session_engine(self):
        if 'session_engine' in self.settings:
            engine = importlib.load_class(self.settings['session_engine'])
            self.session_engine = engine(self.settings["session_secret"],
                    self.settings["session_options"],
                    self.settings["session_timeout"],
                    self.settings["session_cookie_domain"])

    def _setup_template_loaders(self):
        if "template_loader" in self.settings:
            loader = self.settings['template_loader']
        else:
            loader = FileSystemLoader(self.settings['template_dirs'])
        autoescape = bool(self.settings['autoescape'])
        self.jinja_env = Environment(
            loader=loader,
            auto_reload=self.settings['debug'],
            extensions=['workin.utils.jinja2htmlcompress.SelectiveHTMLCompress'],
            autoescape=autoescape, )

    def _setup_installed_apps(self):
        """Auto discovery handlers"""
        if not self.settings.get('installed_apps'):
            return

        for app in self.settings['installed_apps']:
            try:
                importlib.import_module(app + '.handlers')
            except ImportError, e:
                logging.warn("No handlers found in app '%s':"
                        "%s" % (app, e))
            try:
                importlib.import_module(app + '.models')
            except ImportError, e:
                logging.warn("No models/handlers found in app '%s':"
                        "%s" % (app, e))

        self.handlers.extend(Route.routes())

    def _setup_extensions(self):
        """Auto discovery workin extensions"""
        if not self.settings.get('workin_extensions'):
            return

        from workin.extensions import BaseDiscover, find_extensions
        for ext in self.settings['workin_extensions']:
            discovery = find_extensions(ext)
            if isinstance(discovery, BaseDiscover):
                logging.info("Install workin.exts.admin ...")
                discovery.execute(self)


class BaseHandler(Jinja2Mixin, tornado.web.RequestHandler):

    def _populate_context_from_ctxprocessors(self, context):
        ctx = {}
        ctx.update(context)

        for ctx_processor in self.application.context_processors:
            ctx.update(ctx_processor(self))

        return ctx

    def render_string(self, template_name, **context):
        context = self._populate_context_from_ctxprocessors(context)
        return super(BaseHandler, self).render_string(template_name, **context)

    def prepare(self):
        self.application.middleware_manager.run_request_hooks(self)
        super(BaseHandler, self).prepare()

    def finish(self, chunk=None):
        self.application.middleware_manager.run_response_hooks(self)
        super(BaseHandler, self).finish(chunk)


class RequestHandler(BaseHandler, FlashMessageMixin):

    @property
    def db(self):
        return self.application.db

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = Session(self.application.session_engine, self)
        return self._session

    def on_finish(self):
        if self.session:  # and self.session.is_modified:
            self.session.save()

        # remove the sqla-session at the end of each request.
        self.db.remove()

        tornado.web.RequestHandler.on_finish(self)

    def write_json(self, data=None, encoder=json.JSONEncoder):
        if not data:
            data = {}
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data, cls=encoder))

    def get_args(self, key, default=None, type=None):
        if type == list:
            if default is None:
                default = []
            return self.get_arguments(key, default)
        value = self.get_argument(key, default)
        if value and type:
            try:
                value = type(value)
            except ValueError:
                value = default
        return value

    @property
    def is_xhr(self):
        '''True if the request was triggered via a JavaScript XMLHttpRequest.
        This only works with libraries that support the `X-Requested-With`
        header and set it to "XMLHttpRequest".  Libraries that do that are
        prototype, jQuery and Mochikit and probably some more.'''
        return self.request.headers.get('X-Requested-With', '') \
                           .lower() == 'xmlhttprequest'
