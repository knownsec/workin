#!/usr/bin/env python
# coding: utf-8

from workin.database import Base

from sqlalchemy import (Column, Integer, String)


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    content = Column(String(1000))

    def __repr__(self):
        return '<Post: %d>' % self.id
