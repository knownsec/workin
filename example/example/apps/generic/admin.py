#!/usr/bin/env python
# encoding: utf-8

from workin.exts import admin
from workin.forms import Required

from .models import Post


class PostAdmin(admin.BaseAdmin):
    model = Post
    list_columns = ['title', 'content']
    list_columns_names = {
        'title': u'标题',
        'content': u'内容'
    }
    sort_columns = ['title']
    form_validators = {
        'title': [Required()],
        'content': [Required()]
    }
    verbose_names = {
        'title': u'标题',
        'content': u'内容'
    }


admin.site.register(Post, PostAdmin, admin.SystemGroup)
