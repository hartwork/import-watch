# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function

import import_spy
from import_spy import DetectCyclicImports, ReportOnImports


import_spy.reset()
import_spy.register(ReportOnImports(depth=1))
import_spy.register(DetectCyclicImports(fail=False))

print('BEGIN')
import_spy.enable()
import yaml
import yaml
import_spy.disable()
print('END')
print()

import yaml

print('BEGIN')
with import_spy.context():
    from yaml import add_constructor
    from yaml.parser import AliasEvent
    import yaml
    import yaml
    import yaml.parser
print('END')
print()

import yaml

print('BEGIN')
with import_spy.context():
    from cyclic_import_package import a
print('END')
