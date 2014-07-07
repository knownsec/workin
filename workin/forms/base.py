#!/usr/bin/env python
# encoding: utf-8

from wtforms import Form

from workin.forms.utils import MultiValueDict


class BaseForm(Form):
    """
    Usage:

    class HelloForm(BaseForm):
        planet = TextField('name', validators=[Required()])
    """
    def __init__(self, handler=None, obj=None, prefix='', formdata=None, **kwargs):
        if handler:
            formdata = MultiValueDict()
            for name in handler.request.arguments.keys():
                formdata.setlist(name, handler.get_arguments(name))
        Form.__init__(self, formdata, obj=obj, prefix=prefix, **kwargs)
