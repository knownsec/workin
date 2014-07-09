#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.orm import ColumnProperty, class_mapper

from .actions import EditAction, DeleteAction, DetailAction


class AdminSettings(object):
    wysiwyg_editor = 'ckeditor'
    use_datatables_js = True


class BaseAdmin(object):
    model = ''
    list_columns = None
    list_columns_names = {}
    list_actions_column = [EditAction, DetailAction, DeleteAction]
    list_primary_key = False
    form_validators = {}
    verbose_names = {}
    verbose_names_plural = {}

    def __init__(self):
        if self.list_columns is None and self.model:
            self.list_columns = [prop.key for prop in
                    class_mapper(self.model).iterate_properties
                    if isinstance(prop, ColumnProperty)]


class AdminSite(object):
    model_admins = set()
    model_groups = set()

    def register(self, admin_class, group="", **kwargs):
        self.model_admins.add(admin_class)
        self.model_groups.add(group)
