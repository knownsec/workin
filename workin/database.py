#!/usr/bin/env python
# encoding: utf-8


from sqlalchemy.ext.declarative import declarative_base


"""
Usage:

from sqlalchemy import Column, Integer, String

class AnModel(Base):
    __tablename__ = 'an_orm'

    id = Column(Integer, primary_key=True) # has an int id
    name = Column(String) # has a name
    description = Column(String) # has a description
"""
Base = declarative_base()
