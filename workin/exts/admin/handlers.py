#!/usr/bin/env python
# coding: utf-8

from tornado.web import StaticFileHandler
from sqlalchemy.orm import ColumnProperty, class_mapper
from wtforms.fields import (StringField, TextAreaField, IntegerField,
    DateTimeField, DateField, FileField, BooleanField)
from wtforms_components import TimeField

from workin.exceptions import ConfigError
from workin.exts.generic import (TemplateHandler, ListHandler, DetailHandler,
    FormHandler, DeleteHandler, FormMixin)
from workin.forms import BaseForm

from .groups import BaseGroup
from .forms import AdminListForm
from .actions import BULK_ACTIONS_MAP
from . import site


class AdminMixin(object):
    def initialize(self, *args, **kwargs):
        # self.admin_settings = self.application.admin_settings
        # self.template_name = ''.join([self.settings['admin_template_path'], self.template_name])

        self.model_set = {}
        for model_admin in site.model_admins:
            try:
                model = model_admin.model
                class_mapper(model)
                self.model_set.update({model.__name__: (model, model_admin)})
            except:
                pass
        # if len(self.model_set) < 1:
            # raise ConfigError('No models were provided in \'admin_classes\' setting.')

    def get_context_data(self, **kwargs):
        model_groups = site.model_groups
        kwargs['model_groups'] = [group() for group in model_groups]

        grouped_models = []
        for group in model_groups:
            grouped_models.extend(group.model_list)
        orphan_models = [model[0] for model in self.model_set.values() if model[0] not in grouped_models]
        if len(orphan_models) > 0:
            orphan_group = BaseGroup(orphan_models)
            kwargs['model_groups'].append(orphan_group)

        kwargs['model_names'] = self.model_set.keys()
        kwargs['admin_static_url'] = self.admin_static_url

        return super(AdminMixin, self).get_context_data(**kwargs)

    def admin_static_url(self, path, include_host=None, **kwargs):
        """Returns a static URL for the given relative static file path.

        This method requires you set the ``static_path`` setting in your
        application (which specifies the root directory of your static
        files).

        This method returns a versioned url (by default appending
        ``?v=<signature>``), which allows the static files to be
        cached indefinitely.  This can be disabled by passing
        ``include_version=False`` (in the default implementation;
        other static file implementations are not required to support
        this, but they may support other options).

        By default this method returns URLs relative to the current
        host, but if ``include_host`` is true the URL returned will be
        absolute.  If this handler has an ``include_host`` attribute,
        that value will be used as the default for all `static_url`
        calls that do not pass ``include_host`` as a keyword argument.

        """
        self.require_setting("admin_static_path", "admin_static_url")
        get_url = self.settings.get("static_handler_class",
                                    StaticFileHandler).make_static_url

        if include_host is None:
            include_host = getattr(self, "include_host", False)

        if include_host:
            base = self.request.protocol + "://" + self.request.host
        else:
            base = ""

        return base + get_url(self.settings, path, **kwargs)


class AdminModelMixin(AdminMixin):
    def get_model_and_admin(self, **kwargs):
        model_arg = kwargs.get('model', None)
        if model_arg not in self.model_set:
            raise ConfigError('No model provided.')
        self.model, self.model_admin = self.model_set[model_arg]
        return (self.model, self.model_admin,)

    def get(self, *args, **kwargs):
        self.model, self.model_admin = self.get_model_and_admin(**kwargs)
        return super(AdminModelMixin, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.model, self.model_admin = self.get_model_and_admin(**kwargs)
        return super(AdminModelMixin, self).post(*args, **kwargs)

    def get_model_props(self):
        props = []
        mapper = self.get_mapper()
        for prop in mapper.iterate_properties:
            if isinstance(prop, ColumnProperty) and mapper.primary_key[0].name != prop.key:
                props.append(prop)
        if len(props) < 1:
            raise ConfigError('The object has no valid properties.')
        return props

    def get_mapper(self):
        return class_mapper(self.model)

    @property
    def model_primary_key_name(self):
        return class_mapper(self.model_admin.model).primary_key[0].name

    def get_verbose_name(self, prop_key):
        return self.model_admin.verbose_names.get(prop_key, prop_key)

    def get_context_data(self, **kwargs):
        kwargs['model'] = self.model
        return super(AdminModelMixin, self).get_context_data(**kwargs)


class AdminDashboardHandler(AdminMixin, TemplateHandler):
    template_name = 'admin/dash.html'


FORM_FIELD_MAP = {
    'text': TextAreaField,
    'string': StringField,
    'unicode': StringField,
    'unicode_text': TextAreaField,
    'integer': IntegerField,
    'small_integer': IntegerField,
    'big_integer': IntegerField,
    'numeric': IntegerField,
    'float': IntegerField,
    'datetime': DateTimeField,
    'date': DateField,
    'time': TimeField,
    'large_binary': FileField,
    'enum': StringField,
    'boolean': BooleanField,
}


class AdminFormMixin(FormMixin):
    def get_form_class(self):
        class AddForm(BaseForm):
            pass
        form_class = AddForm
        if not hasattr(self.model_admin, 'form_fields'):
            props = self.get_model_props()
            for prop in props:
                form_field = FORM_FIELD_MAP.get(prop.columns[0].type.__visit_name__, StringField)
                validators = self.model_admin.form_validators.get(prop.key, [])
                label = self.get_verbose_name(prop.key)
                setattr(AddForm, prop.key, form_field(label, validators))
        return form_class


class AdminAddHandler(AdminModelMixin, AdminFormMixin, FormHandler):
    template_name = 'admin/admin_add.html'

    def form_valid(self, form):
        new_obj = self.model(**form.data)
        self.db.add(new_obj)
        self.db.commit()
        self.db.refresh(new_obj)
        self.object_id = new_obj.id
        self.add_new = self.get_argument('add_new', False)
        return super(AdminAddHandler, self).form_valid(form)

    def get_success_url(self):
        if self.add_new:
            return self.reverse_url('admin_add', self.model.__name__)
        return self.reverse_url('admin_detail', self.model.__name__, self.object_id)


class AdminDetailHandler(AdminModelMixin, DetailHandler):
    template_name = 'admin/admin_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['property_map'] = self.get_property_map()
        return super(AdminDetailHandler, self).get_context_data(**kwargs)

    def get_property_map(self):
        property_map = {}
        obj = self.get_object()
        props = self.get_model_props()
        for prop in props:
            label = self.get_verbose_name(prop.key)
            property_map[label] = getattr(obj, prop.key)
        return property_map


class AdminDeleteHandler(AdminModelMixin, DeleteHandler):
    def get_context_data(self, **kwargs):
        return super(AdminDeleteHandler, self).get_context_data(**kwargs)


class TableManager(object):
    pass


class Table(object):
    def __init__(self, object_list, model_admin):
        self.object_list = object_list
        self.model_admin = model_admin
        self.rows = []
        self.construct_rows()

    def construct_rows(self):
        if self.model_admin.list_primary_key:
            if self.model_primary_key_name not in self.model_admin.list_columns:
                self.model_admin.list_columns.insert(0, self.model_primary_key_name)
        self.resolve_first_row_cells()
        for obj in self.object_list:
            row = Row(obj, self.model_admin)
            self.rows.append(row)
        if self.model_admin.list_actions_column:
            self.first_row.append(Cell('Actions'))

    def resolve_first_row_cells(self):
        self.first_row = []
        for column_name in self.model_admin.list_columns:
            if column_name in self.model_admin.list_columns_names:
                cell = Cell(self.model_admin.list_columns_names[column_name])
            else:
                cell = Cell(column_name)
            self.first_row.append(cell)

    @property
    def header(self):
        return self.model_admin.model.__name__


class Row(object):
    def __init__(self, obj, model_admin):
        self.obj = obj
        self.model_admin = model_admin
        self.cells = []
        self.construct_cells()

    def construct_cells(self):
        for column_name in self.model_admin.list_columns:
            if hasattr(self.obj, column_name):
                value = getattr(self.obj, column_name)
                cell = Cell(value)
                self.cells.append(cell)
            else:
                raise ConfigError('Provided column_name "%s" is not valid.' % column_name)

    @property
    def obj_primary_key(self):
        primary_key_name = self.obj.__mapper__.primary_key[0].name
        return getattr(self.obj, primary_key_name)

    def __iter__(self):
        pass


class Cell(object):
    def __init__(self, value, link=None):
        self.value = value
        self.link = link

    @property
    def has_link(self):
        return bool(self.link)


class AdminListHandler(AdminModelMixin, FormMixin, ListHandler):
    template_name = 'admin/admin_list.html'
    paginate_by = 10
    form_class = AdminListForm
    # queryset = Post.query.order_by(desc(Post.created))

    def post(self, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        super(AdminListHandler, self).post(*args, **kwargs)
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = super(AdminListHandler, self).get_form(form_class)
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        chosen_action = form.data['action']
        action = BULK_ACTIONS_MAP[chosen_action]
        id_list = [int(x) for x in self.get_arguments('rows[]')]
        action.process_list_choices(self.db, self.model, id_list)
        return super(AdminListHandler, self).form_valid(form)

    def get_context_data(self, **kwargs):
        form = kwargs.pop('form', None)
        if form is None:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
        kwargs['form'] = form
        kwargs['table'] = Table(self.object_list, self.model_admin)
        return super(AdminListHandler, self).get_context_data(**kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(AdminListHandler, self).get_form(form_class)
        for obj in self.object_list:
            pk = (obj.id, '')
            form.rows.choices.append(pk)
        return form

    def get_success_url(self):
        page_num = self.kwargs.get('page', 1)
        return self.reverse_url('admin_list', self.model.__name__, page_num)


class AdminEditHandler(AdminModelMixin, AdminFormMixin, DetailHandler):
    template_name = 'admin/admin_edit.html'
    initial = {}

    def post(self, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        super(AdminEditHandler, self).post(*args, **kwargs)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        props = self.get_model_props()
        for prop in props:
            setattr(self.object, prop.key, form.data[prop.key])
        self.db.commit()
        self.db.refresh(self.object)
        return super(AdminEditHandler, self).form_valid(form)

    def get_initial(self):
        props = self.get_model_props()
        for prop in props:
            self.initial[prop.key] = getattr(self.object, prop.key)
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        kwargs['form'] = form
        return super(AdminEditHandler, self).get_context_data(**kwargs)

    def get_success_url(self):
        return self.reverse_url('admin_detail', self.model.__name__, self.object.id)
