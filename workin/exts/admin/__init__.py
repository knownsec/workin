#!/usr/bin/env python
# encoding: utf-8

from .base import BaseAdmin, AdminSite

site = AdminSite()

__all__ = ['BaseAdmin', 'site']
