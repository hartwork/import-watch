#! /usr/bin/env python2
# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from textwrap import dedent

from setuptools import find_packages, setup

_classifiers = dedent("""\
    Development Status :: 3 - Alpha

    Intended Audience :: Developers

    License :: OSI Approved :: MIT License

    Natural Language :: English

    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8

    Programming Language :: Python :: Implementation :: CPython
""")

_description = 'Trace module imports and detect/deny cyclic imports at runtime'


if __name__ == '__main__':
    setup(
            name='import-watch',
            url='https://github.com/hartwork/import-watch',
            description=_description,
            long_description=_description,
            license='MIT',
            version='2.0.0',
            author='Sebastian Pipping',
            author_email='sebastian@pipping.org',
            packages=find_packages(),
            classifiers=[c for c in _classifiers.split('\n') if c],
            )
