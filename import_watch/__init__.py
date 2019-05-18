# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function

import warnings
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from functools import wraps

_original_import = __builtins__['__import__']

_import_stack = []

_import_watchers = []

_is_enabled = False

_ImportData = namedtuple('_ImportData', [
    'module_name',
    'symbols_tuple_or_none',
])


def _extract_import_data(args):
    return _ImportData(module_name=args[0], symbols_tuple_or_none=args[3])


def _format_import_data(import_data):
    if import_data.symbols_tuple_or_none is None:
        return 'import {}'.format(import_data.module_name)
    else:
        return 'from {} import {}'.format(
            import_data.module_name, ', '.join(
                import_data.symbols_tuple_or_none))


@wraps(_original_import)
def _wrapped_import(*args, **kvargs):
    global _import_stack

    for watcher in _import_watchers:
        watcher.process(args, kvargs, _import_stack)

    _import_stack.append(_extract_import_data(args))
    try:
        module = _original_import(*args, **kvargs)
    finally:
        _import_stack.pop()

    return module


class _ImportWatcher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, args, kvargs, history):
        pass


class _TracingWatcher(_ImportWatcher):
    def __init__(self, depth=None):
        self._max_depth = depth
        self._prev_depth = None

    def process(self, args, kvargs, history):
        depth = len(history)
        indent = '  ' * depth

        depth += 1

        if self._max_depth is None or depth <= self._max_depth:
            import_data = _extract_import_data(args)
            print(indent + _format_import_data(import_data))
        elif self._max_depth is not None and depth == self._max_depth + 1 \
                and depth > self._prev_depth:
            print(indent + '[..]')

        self._prev_depth = depth


class CyclicImportWarning(UserWarning):
    pass


class CyclicImportError(ImportError):
    pass


class _CycleDetectionWatcher(_ImportWatcher):
    def __init__(self, fail=False):
        self._fail = fail

    def handle_cyclic_import(self, history_slice):
        message = 'Cyclic import detected:\n{}'.format('\n'.join(
            '  > {}{}'.format('  ' * i, _format_import_data(import_data))
            for i, import_data in enumerate(history_slice)))
        warnings.warn(message, CyclicImportWarning, stacklevel=4)
        if self._fail:
            raise CyclicImportError(
                "Cyclic import for module '{}'".format(
                    history_slice[-1].module_name))

    @staticmethod
    def _all_names_from(import_data):
        if import_data.symbols_tuple_or_none is None:
            return (import_data.module_name,)
        else:
            return (import_data.module_name,) + tuple(
                '{}.{}'.format(import_data.module_name, symbol)
                for symbol in import_data.symbols_tuple_or_none)

    def _find_cyclic_import(self, args, history):
        new_import_data = _extract_import_data(args)
        all_new_names = self._all_names_from(new_import_data)

        for i, old_import_data in enumerate(history):
            past_names = self._all_names_from(old_import_data)
            for a in all_new_names:
                for b in past_names:
                    if a == b:
                        return history[i:] + [new_import_data]

        return None

    def process(self, args, kvargs, history):
        history_slice = self._find_cyclic_import(args, history)
        if history_slice:
            self.handle_cyclic_import(history_slice)


def _register(watcher):
    _import_watchers.append(watcher)


def _enable():
    global _is_enabled

    __builtins__['__import__'] = _wrapped_import
    _is_enabled = True


def _disable():
    global _is_enabled

    __builtins__['__import__'] = _original_import
    _is_enabled = False


def reset():
    global _import_watchers

    _disable()
    _import_watchers = []


def deny_cyclic_imports():
    _register(_CycleDetectionWatcher(fail=True))
    _enable()


def trace_imports(depth=None):
    _register(_TracingWatcher(depth=depth))
    _enable()


def warn_about_cyclic_imports():
    _register(_CycleDetectionWatcher(fail=False))
    _enable()


__all__ = []  # i.e. discourage use of star imports
