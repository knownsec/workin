#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.orm import class_mapper

from workin.exceptions import ConfigError


class BaseGroup(object):
    label = 'Models'
    model_list = []
    glyphicon = 'bar-chart-o'

    def __init__(self, model_list=None):
        self.add_model_list(model_list)

    @property
    def model_names(self):
        return [model.__name__ for model in self.model_list]

    @property
    def plural_names(self):
        plucont = {}
        for model in self.model_list:
            plural = model.__dict__.get('admin_dashboard_plural', None)
            if plural is None:
                plural = model.__name__
            plucont.update({model.__name__: plural})
        return plucont

    def add_model(self, model):
        try:
            class_mapper(model)
        except:
            raise ConfigError('%s is not a valid model.')
        if model not in self.model_list:
            self.model_list.append(model)

    def add_model_list(self, model_list):
        if model_list is not None:
            for model in model_list:
                self.add_model(model)


class SystemGroup(BaseGroup):
    label = 'System Management'
    glyphicon = 'gears'
