#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from workin.utils import importlib

NOW = datetime.datetime.now


class AuthHandlerMixin(object):

    def __init__(self, *args, **kwargs):
        super(AuthHandlerMixin, self).__init__(*args, **kwargs)

        ext_path = 'workin.exts.auth'
        self.require_setting('auth_user_model', ext_path)
        self.require_setting('auth_session_key', ext_path)
        self.require_setting('auth_cookie_key', ext_path)

        self._auth_user = importlib.load_class(self.settings['auth_user_model'])
        self._auth_session_key = self.settings['auth_session_key']
        self._auth_cookie_key = self.settings['auth_cookie_key']

    def authenticate(self, username, password):
        """Authenticates against `username` and `password`."""
        try:
            user = (self.db.query(self._auth_user)
                    .filter(self._auth_user.username == username).one())
            if user.check_password(password):
                return user
            else:
                return None
        except (NoResultFound, MultipleResultsFound):
            return None

    def register(self, **kwargs):
        """Create an user.

        If `next_url` is specified, redirect to it at last.
        """
        next_url = kwargs.pop('next_url', None)
        password = kwargs.pop('password')

        user = self._auth_user(**kwargs)
        user.set_password(password)
        user.date_joined = NOW()
        self.db.add(user)
        self.db.commit()

        if next_url:
            self.redirect(next_url)

    def login(self, user, next_url=None):
        """Persist a user id and send session id as a cookie.

        This way a user doesn't have to reauthenticate on every request.
        If `next_url` is specified, redirect to it at last.
        """
        user.last_login = NOW()
        self.db.merge(user)
        self.db.commit()

        self.session[self._auth_session_key] = user.id
        self.session.save()

        self.set_secure_cookie(self._auth_cookie_key, self.session.session_id)
        if next_url:
            self.redirect(next_url)

    def logout(self, next_url=None):
        """Removes the authenticated user's ID and clear cookies.

        If `next_url` is specified, redirect to it at last.
        """
        self.session.pop(self._auth_session_key, None)
        self.session.save()

        self.clear_cookie(self._auth_cookie_key)
        if next_url:
            self.redirect(next_url)

    def get_current_user(self):
        if self._auth_session_key in self.session:
            user_id = self.session[self._auth_session_key]
            user = (self.db.query(self._auth_user)
                    .filter(self._auth_user.id == user_id).first())
            return user
        return None
