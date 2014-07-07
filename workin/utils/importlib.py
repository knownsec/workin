# Taken from Python 2.7 with permission from/by the original author.
import sys


def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]


def load_class(path):
    """
    Load class from path.
    """

    mod_name, klass_name = None, None

    try:
        mod_name, klass_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except AttributeError as e:
        raise RuntimeError("Error importing {0}: '{1}'".format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise RuntimeError('Module "{0}" does not define a "{1}" class'.format(mod_name, klass_name))

    return klass


class LazyImport:
    """lazy import module"""
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, func_name):
        if self.module is None:
            self.module = import_module(self.module_name)
        return getattr(self.module, func_name)

lazy_import = LazyImport
