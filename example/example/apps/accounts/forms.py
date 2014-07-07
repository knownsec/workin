#!/usr/bin/env python
# coding: utf-8

from workin.forms import BaseForm, TextField, Required


class UserForm(BaseForm):
    username = TextField('username', validators=[Required()])
    phone = TextField('phone', validators=[Required()])
