#!/usr/bin/env python
# coding: utf-8

from workin.database import Base

from sqlalchemy import (Column, Integer, String)


class TestUser(Base):
    __tablename__ = 'test_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(1000))
    phone = Column(String(1000))

    def __repr__(self):
        return '<User: %d>' % self.id
