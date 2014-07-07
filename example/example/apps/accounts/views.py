#!/usr/bin/env python
# coding: utf-8

from workin.web import RequestHandler
from workin.routes import route
from workin.exts.generic import (ListHandler, DetailHandler, EditHandler,
        DeleteHandler)

from .forms import UserForm
from .models import TestUser


@route(r'/login', name='login')
class Login(RequestHandler):

    def get(self):
        users = self.db.query(TestUser)
        self.render('accounts/list.html', users=users)


@route(r'/list/', name='list')
class List(ListHandler, RequestHandler):
    """Demo for generic view"""
    model = TestUser
    template_name = 'accounts/list.html'


@route(r'/detail/(?P<id>.*)', name='detail')
class Detail(DetailHandler, RequestHandler):
    """Demo for generic view"""
    model = TestUser
    template_name = 'accounts/detail.html'


@route(r'/edit/(?P<id>.*)', name='user-edit')
class EditUser(EditHandler, RequestHandler):
    """Demo for generic view"""
    model = TestUser
    form_class = UserForm
    template_name = 'accounts/edit.html'


@route(r'/delete/(?P<id>.*)', name='user-delete')
class DeleteUser(DeleteHandler, RequestHandler):
    """Demo for generic view"""
    model = TestUser
    form_class = UserForm
    template_name = 'accounts/edit.html'
    success_url = '/list'


@route(r'/index', name='index')
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
