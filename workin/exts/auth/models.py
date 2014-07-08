#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Unicode

from workin.database import Base


class User(Base):
    """User model."""

    # a module/class object which has functions/methods
    # `make_password` and `check_password` to handle password securely
    import hasher
    HASHER = hasher

    __tablename__ = 'test_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Unicode(100), nullable=False, index=True)
    password = Column(String(100), nullable=False)
    email = Column(Unicode(100), nullable=False)

    def __repr__(self):
        return '<User %s>' % self.id

    def set_password(self, password):
        self.password = self.HASHER.make_password(password)

    def check_password(self, password):
        return self.HASHER.check_password(password, self.password)
