#!/usr/bin/env python
# -*- coding: utf-8 -*-

from workin.routes import route
from workin.web import RequestHandler
from workin.exts.auth import AuthHandlerMixin, login_required


class BaseHandler(AuthHandlerMixin, RequestHandler):
    pass


@route(r'/', name='index')
class Index(BaseHandler):
    def get(self):
        self.render('accounts/index.html')


@route(r'/admin', name='admin')
class Admin(BaseHandler):
    @login_required(login_url='/login')
    def get(self):
        self.render('accounts/admin.html')


@route(r'/register', name='register')
class Register(BaseHandler):
    def get(self):
        self.render('accounts/register.html')

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        self.register(username=username, password=password,
                      email=email, next_url='/')


@route(r'/login', name='login')
class Login(BaseHandler):
    def get(self):
        self.render('accounts/login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next')
        user = self.authenticate(username, password)
        if user:
            self.login(user, next_url=next_url)
        else:
            self.redirect('/register')


@route(r'/logout', name='logout')
class Logout(BaseHandler):
    def get(self):
        self.logout(next_url='/')
