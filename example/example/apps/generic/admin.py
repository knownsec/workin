#!/usr/bin/env python
# encoding: utf-8

from workin.exts import admin
from workin.forms import Required

from .models import Post


class PostAdmin(admin.BaseAdmin):
    model = Post
    list_columns = ['title', 'content']
    form_validators = {
        'title': [Required()],
        'content': [Required()]
    }

admin.site.register(PostAdmin)
