#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.orm import class_mapper

from workin.exceptions import ConfigError


class BaseGroup(object):
    label = 'Models'
    model_list = None
    glyphicon = 'bar-chart-o'

    def __init__(self, model_list=None):
        if model_list is not None:
            for model in model_list:
                try:
                    class_mapper(model)
                except:
                    raise ConfigError('%s is not a valid model')
            self.model_list = model_list

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
