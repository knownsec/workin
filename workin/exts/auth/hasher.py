#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcrypt


def make_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password, hashed):
    return bcrypt.hashpw(password, hashed) == hashed
