#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy.orm.exc import NoResultFound

from workin.exceptions import ImproperlyConfigured
from .base import GenericHandler, TemplateResponseMixin, ContextMixin


class SingleObjectMixin(ContextMixin):
    """
    Provides the ability to retrieve a single object for further manipulation.
    """
    model = None
    queryset = None
    slug_field = None
    context_object_name = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        slug_field = self.get_slug_field()
        if pk is not None:
            queryset = queryset.filter(self.model.id == pk)

        # Next, try looking up by slug.
        elif slug is not None and slug_field is not None:
            queryset = queryset.filter(slug_field == slug)

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.one()
        except NoResultFound:
            raise ValueError("No %(verbose_name)s found matching the query" %
                          {'verbose_name': str(self.model)})
        return obj

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.

        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overriden.
        """
        if self.queryset is None:
            if self.model:
                return self.db.query(self.model)
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset

    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field

    def get_context_object_name(self, obj):
        """
        Get the name to use for the object.
        """
        if self.context_object_name:
            return self.context_object_name
        else:
            return None

    def get_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super(SingleObjectMixin, self).get_context_data(**context)


class BaseDetailHandler(SingleObjectMixin, GenericHandler):
    """
    A base view for displaying a single object
    """
    def get(self, *args, **kwargs):
        super(BaseDetailHandler, self).get(*args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render(context)


class DetailHandler(TemplateResponseMixin, BaseDetailHandler):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
