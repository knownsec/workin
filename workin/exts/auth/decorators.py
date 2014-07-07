#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import types

import tornado.web


def login_required(method=None, login_url=None):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to `login_url` or
    to the configured `login url <RequestHandler.get_login_url>`.
    """
    def outer(method):
        @functools.wraps(method)
        def inner(self, *args, **kwargs):
            # if `login_url` is specified, override `self.get_login_url` to
            # reuse `tornado.web.authenticated` with explicit `login_url`.
            if login_url:
                self.get_login_url = types.MethodType(lambda self: login_url,
                                                      self)
            _ = tornado.web.authenticated(method)
            return _(self, *args, **kwargs)
        return inner

    if method:
        return outer(method)
    return outer
