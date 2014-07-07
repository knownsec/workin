#!/usr/bin/env python
# encoding: utf-8


class SessionData(dict):
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key


class Session(SessionData):
    def __init__(self, session_engine, request_handler):

        self.session_engine = session_engine
        self.request_handler = request_handler

        try:
            current_session = session_engine.get(request_handler)
        except InvalidSessionException:
            current_session = session_engine.get()
        for key, data in current_session.iteritems():
            self[key] = data
        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

    def save(self):
        self.session_engine.set(self.request_handler, self)


class InvalidSessionException(Exception):
    pass
