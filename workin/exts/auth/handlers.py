#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .settings import (
    DB, USER, SESSION, SESSION_KEY, COOKIE_KEY
)


class AuthHandlerMixin(object):

    def authenticate(self, username, password):
        """Authenticates against `username` and `password`."""
        try:
            user = DB.query(USER).filter(USER.username == username).one()
            if user.check_password(password):
                return user
            else:
                return None
        except (NoResultFound, MultipleResultsFound):
            return None

    # def register(self, username, password, *args, **kwargs):
    def register(self, **kwargs):
        """Create an user.

        If `next_url` is specified, redirect to it at last.
        """
        next_url = kwargs.pop('next_url', None)
        password = kwargs.pop('password')

        user = USER(**kwargs)
        user.set_password(password)
        DB.add(user)
        DB.commit()

        if next_url:
            self.redirect(next_url)

    def login(self, user, next_url=None):
        """Persist a user id and send session id as a cookie.

        This way a user doesn't have to reauthenticate on every request.
        If `next_url` is specified, redirect to it at last.
        """
        if not hasattr(self, 'session'):
            self.session = SESSION()
        self.session[SESSION_KEY] = user.id
        self.set_secure_cookie(COOKIE_KEY, SESSION_KEY)
        if next_url:
            self.redirect(next_url)

    def logout(self, next_url=None):
        """Removes the authenticated user's ID and clear cookies.

        If `next_url` is specified, redirect to it at last.
        """
        if hasattr(self, 'session'):
            self.session.pop(SESSION_KEY, None)
        self.clear_cookie(COOKIE_KEY)
        if next_url:
            self.redirect(next_url)

    def get_current_user(self):
        session_key = self.get_secure_cookie(COOKIE_KEY)
        if hasattr(self, 'session') and session_key in self.session:
            user_id = self.session[session_key]
            user = DB.query(USER).filter(USER.id == user_id).first()
            return user
        return None
