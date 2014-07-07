#!/usr/bin/env python
# encoding: utf-8

import tornado


class FlashMessageMixin(object):
    """
        Store a message between requests which the user needs to see.

        views
        -------

        self.flash("Welcome back, %s" % username, 'success')

        base.html
        ------------

        {% set messages = handler.get_flashed_messages() %}
        {% if messages %}
        <div id="flashed">
            {% for category, msg in messages %}
            <span class="flash-{{ category }}">{{ msg }}</span>
            {% end %}
        </div>
        {% end %}
    """
    def flash(self, message, category='message'):
        messages = self.messages()
        messages.append((category, message))
        self.set_secure_cookie('flash_messages', tornado.escape.json_encode(messages))

    def messages(self):
        messages = self.get_secure_cookie('flash_messages')
        messages = tornado.escape.json_decode(messages) if messages else []
        return messages

    def get_flashed_messages(self):
        messages = self.messages()
        self.clear_cookie('flash_messages')
        return messages
