#!/usr/bin/env python
# encoding: utf-8


from workin.exceptions import ImproperlyConfigured
from .base import TemplateResponseMixin, ContextMixin, GenericHandler
from .detail import BaseDetailHandler, SingleObjectMixin


class FormMixin(ContextMixin):
    """
    A mixin that provides a way to show and handle a form in a request.
    """

    initial = {}
    form_class = None
    success_url = None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {}
        kwargs.update(self.get_initial())
        arguments = {k: v[0] for k, v in self.request.arguments.iteritems()}
        kwargs.update(arguments)
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if not self.success_url:
            raise AttributeError("No URL to redirect to. Provide a success_url.")
        return self.success_url

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        return self.redirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render(self.get_context_data(form=form))


class ProcessFormHandler(GenericHandler):
    """
    A mixin that renders a form on GET and processes it on POST.
    """
    def get(self, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        super(ProcessFormHandler, self).get(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render(self.get_context_data(form=form))

    def post(self, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        super(ProcessFormHandler, self).post(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.validate():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormHandler(FormMixin, ProcessFormHandler):
    """
    A base view for displaying a form
    """


class FormHandler(TemplateResponseMixin, BaseFormHandler):
    """
    A view for displaying a form, and rendering a template response.
    """


class ProcessEditHandler(SingleObjectMixin, GenericHandler):

    def get(self, *args, **kwargs):
        super(ProcessEditHandler, self).get(*args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render(context)


class BaseEditHandler(FormMixin, ProcessEditHandler):
    """
    A base view for displaying a form
    """


class EditHandler(TemplateResponseMixin, BaseEditHandler):
    """
    A view for displaying a form, and rendering a template response.
    """


class DeletionMixin(object):
    """
    A mixin providing the ability to delete objects
    """
    success_url = None

    def delete(self, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        __import__('pdb').set_trace()
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.db.delete(self.object)
        self.db.commit()
        return self.redirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, *args, **kwargs):
        super(DeletionMixin, self).post(*args, **kwargs)
        return self.delete(*args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseDeleteHandler(DeletionMixin, BaseDetailHandler):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class DeleteHandler(TemplateResponseMixin, BaseDeleteHandler):
    """
    View for deleting an object retrieved with `self.get_object()`,
    with a response rendered by template.
    """
