#!/usr/bin/env python
# encoding: utf-8

import collections
from math import ceil


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator(object):
    """A helper class for paginating object list. Example::

    .. sourcecode:: python

        page_number = 1
        user_list = db.session.query(Uesr).all()
        user_pagnatior = Paginator(user_list, per_page=20)
        current_page = user_pagnatior.page(page_number)

        for user in current_page:
            print user

        if current_page.has_next():
            print current_page.next_page_number

        if current_page.has_previous():
            print current_page.previous_page_number

        self.render('use_in_jinja2.html', pager=current_page)

    .. sourcecode:: html+jinja2

        {% macro render_pagination(pager, endpoint_name) %}
            <div class="pagination">
                {% if pager.has_previous() %}
                <a href="{{ reverse_url(endpoint_name) }}?page={{ pager.previous_page_number() }}">Prev</a>
                {% endif %}
                {% for number in pager.paginator.page_range %}
                    {% if number != pager.number %}
                <a href="{{ reverse_url(endpoint_name) }}?page={{ number }}">{{ number }}</a>
                    {% else %}
                <a class="current_page">{{ number }}</a>
                    {% endif %}
                {% endfor %}
                {% if pager.has_next() %}
                <a href="{{ reverse_url(endpoint_name) }}?page={{ pager.next_page_number() }}">Next</a>
                {% endif %}
            </div>
        {% endmacro %}
        {{ render_pagination(pager, 'user_list') }}

    :param object_list: the list for paginate.
    :param per_page: how many objects put in each page.
    :param orphans: The minimum number of items allowed on the last page.
                    If the last page have a number of items less than/equal to `orphans`,
                    those items will be added to the previous page.
    :param allow_empty_first_page: :class:`~workin.exts.generic.pagination.Paginator`
                                   returns page even though no objects by default.
                                   When this argument set to `False`, it
                                   raises :class:`~workin.exts.generic.pagination.EmptyPage`
                                   instead.
    """

    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None

    def validate_number(self, number):
        """
        Validates the given 1-based page number.

        :param number: the number of page.
        :returns: the page number itself.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self._get_page(self.object_list[bottom:top], number, self)

    def _get_page(self, *args, **kwargs):
        """
        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
        return self._count
    #: the total number of object_list.
    count = property(_get_count)

    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    #: the total number pages.
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)
    #: range of pagination
    page_range = property(_get_page_range)


class Page(collections.Sequence):

    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page
