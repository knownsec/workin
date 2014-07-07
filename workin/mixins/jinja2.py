#!/usr/bin/env python
# encoding: utf-8

from tornado import escape


class Jinja2Mixin(object):

    def render_string(self, template_name, **context):
        self.require_setting("template_path", "render")
        default_context = {
            'handler': self,
            'request': self.request,
            'current_user': self.current_user,
            'static_url': self.static_url,
            'xsrf_form_html': self.xsrf_form_html,
            'reverse_url': self.reverse_url,
        }

        escape_context = {
            'escape': escape.xhtml_escape,
            'xhtml_escape': escape.xhtml_escape,
            'url_escape': escape.url_escape,
            'json_encode': escape.json_encode,
            'squeeze': escape.squeeze,
            'linkify': escape.linkify,
        }
        context.update(default_context)
        context.update(escape_context)
        context.update(self.ui)     # Enabled tornado UI modules and methods.
        template = self.application.jinja_env.get_template(
            template_name)
        return template.render(**context)
