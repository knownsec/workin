#!/usr/bin/env python
# coding: utf-8

from workin.routes import route
from workin.exts.generic import (ListHandler, DetailHandler,
        DeleteHandler, TemplateHandler, FormHandler)

from .models import Post
from .forms import LoginForm


@route(r'/', name='generic-home')
class HomeHandler(TemplateHandler):
    template_name = 'home.html'


@route(r'/posts/', name='generic-posts')
class BlogHandler(ListHandler):
    template_name = 'blog.html'
    paginate_by = 10
    context_object_name = 'post_list'
    model = Post


@route(r'/post/?P<id>.*', name='generic-post')
class PostHandler(DetailHandler):
    template_name = 'post.html'
    model = Post
    context_object_name = 'post'


@route(r'/login/', name='generic-login')
class LoginHandler(FormHandler):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.set_secure_cookie('user', form.data['username'])
        return super(LoginHandler, self).form_valid(form)


@route(r'/post/del/?P<id>.*', name='generic-post-del')
class DeletePostHandler(DeleteHandler):
    template_name = 'confirm_delete.html'
    model = Post
    success_url = '/posts/'
