# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function

import warnings
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from functools import wraps
from collections import namedtuple


_original_import = __builtins__['__import__']

_import_stack = []

_import_spies = []

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

    for spy in _import_spies:
        spy.process(args, kvargs, _import_stack)

    _import_stack.append(_extract_import_data(args))
    try:
        module = _original_import(*args, **kvargs)
    finally:
        _import_stack.pop()

    return module


class ImportSpy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, args, kvargs, history):
        pass


class ReportOnImports(ImportSpy):
    def __init__(self, depth=None):
        self._max_depth = depth
        self._prev_depth = None

    def process(self, args, kvargs, history):
        depth = len(history)
        indent = '  ' * depth

        if self._max_depth is None or depth <= self._max_depth:
            import_data = _extract_import_data(args)
            print(indent + _format_import_data(import_data))
        elif self._max_depth is not None and depth == self._max_depth + 1 \
                and depth > self._prev_depth:
            print(indent + '[..]')
        self._prev_depth = depth


class CyclicImportWarning(UserWarning):
    pass


class DetectCyclicImports(ImportSpy):
    def __init__(self, fail=False):
        self._fail = fail

    def handle_cyclic_import(self, history_slice):
        message = 'Cyclic import detected:\n{}'.format('\n'.join(
            '  > {}{}'.format('  ' * i, _format_import_data(import_data))
            for i, import_data in enumerate(history_slice)))
        warnings.warn(message, CyclicImportWarning, stacklevel=4)
        if self._fail:
            raise ImportError

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


def _instance(clazz_or_instance):
    if isinstance(clazz_or_instance, type):
        return clazz_or_instance()
    return clazz_or_instance


def _list_of_instances(list_or_item):
    if list_or_item is None:
        return []
    if isinstance(list_or_item, (list, tuple)):
        return [_instance(item) for item in list_or_item]
    return [_instance(list_or_item)]


def register(spy):
    _import_spies.append(_instance(spy))


def enable():
    global _is_enabled

    __builtins__['__import__'] = _wrapped_import
    _is_enabled = True


def disable():
    global _is_enabled

    __builtins__['__import__'] = _original_import
    _is_enabled = False


def reset():
    global _import_spies

    disable()
    _import_spies = []


@contextmanager
def context(spies=None, enabled=True):
    global _is_enabled
    global _import_spies

    if _is_enabled and not enabled:
        disable()
        yield
        enable()
    elif not _is_enabled and enabled:
        if spies is not None:
            spies_backup = _import_spies
            _import_spies = _list_of_instances(spies)
        enable()

        yield

        disable()
        if spies is not None:
            _import_spies = spies_backup
    else:
        yield


register(ReportOnImports)


__all__ = []  # i.e. discourage use of star imports
