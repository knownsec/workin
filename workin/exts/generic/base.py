#!/usr/bin/env python
# encoding: utf-8

import tornado


class ContextMixin(object):
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data as the template context.
    """

    def get_context_data(self, **kwargs):
        if 'handler' not in kwargs:
            kwargs['handler'] = self
        return kwargs


class GenericHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def post(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @property
    def db(self):
        return self.application.db


class TemplateResponseMixin(object):
    """
    A mixin that can be used to render a template.
    """
    template_name = None

    def render(self, context):
        return super(TemplateResponseMixin, self).render(self.template_name, **context)


class TemplateHandler(TemplateResponseMixin, ContextMixin, GenericHandler):
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the url conf.
    """
    def get(self, *args, **kwargs):
        super(TemplateHandler, self).get(*args, **kwargs)
        context = self.get_context_data(**kwargs)
        return self.render(context)
