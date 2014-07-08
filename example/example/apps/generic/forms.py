#!/usr/bin/env python
# coding: utf-8

from workin.forms import BaseForm, TextField, Required


class LoginForm(BaseForm):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
