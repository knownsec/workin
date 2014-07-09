#!/usr/bin/env python
# coding: utf-8

from wtforms import widgets
from wtforms.fields import SelectMultipleField, SelectField
from wtforms.widgets.core import HTMLString

from workin.forms import BaseForm


class SelectCheckbox(widgets.CheckboxInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return HTMLString('<input %s>' % self.html_params(name=field.name + '[]', **kwargs))


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = SelectCheckbox()


class AdminListForm(BaseForm):
    rows = MultiCheckboxField(choices=[], coerce=int)
    action = SelectField(choices=[('delete', 'delete')])
