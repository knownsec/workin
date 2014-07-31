#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from django_hasher import check_password, make_password
except ImportError:
    import bcrypt

    def make_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(password, hashed):
        return bcrypt.hashpw(password, hashed) == hashed
