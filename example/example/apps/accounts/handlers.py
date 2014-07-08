#!/usr/bin/env python
# coding: utf-8

from workin.web import RequestHandler
from workin.routes import route

from .forms import UserForm
from .models import TestUser


@route(r'/accounts/', name='acccounts')
class IndexHandler(RequestHandler):
    def get(self):
        form = UserForm()
        self.render('accounts/user.html', form=form)

    def post(self):
        form = UserForm(self)
        if form.validate():
            user = TestUser(username=form.username.data, phone=form.phone.data)
            self.db.add(user)
            self.db.commit()

            self.write('Hello %s' % form.username.data)
        else:
            self.render('accounts/user.html', form=form)
