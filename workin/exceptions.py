#!/usr/bin/env python
# encoding: utf-8

"""
Workin exception module
"""
try:
    from exceptions import Exception, StandardError
except ImportError:
    # Python 3
    StandardError = Exception


class WorkinError(StandardError):
    """Exception related to operation with torngas."""


class ArgumentError(WorkinError):
    """Arguments error"""


class ConfigError(WorkinError):
    """raise config error"""
    def __repr__(self):
        return 'Configuration for %s is missing or invalid' % self.args[0]


class ImproperlyConfigured(WorkinError):
    """Improperly Configured"""


class UrlError(WorkinError):
    """route write error"""


from tornado.web import HTTPError


class APIError(HTTPError):
    """API error handling exception

    API server always returns formatted JSON to client even there is
    an internal server error.
    """

    def __init__(self, status_code, log_message=None, *args, **kwargs):
        super(APIError, self).__init__(status_code, log_message, *args, **kwargs)
