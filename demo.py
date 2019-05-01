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
import yaml  # noqa: E402
import yaml  # noqa: E402, F811
import_spy.disable()
print('END')
print()

import yaml  # noqa: E402, F811

print('BEGIN')
with import_spy.context():
    from yaml import add_constructor  # noqa: E402, F401
    from yaml.parser import AliasEvent  # noqa: E402, F401
    import yaml  # noqa: E402, F811
    import yaml  # noqa: E402, F811
    import yaml.parser  # noqa: E402
print('END')
print()

import yaml  # noqa: E402, F401

print('BEGIN')
with import_spy.context():
    from cyclic_import_package import a  # noqa: E402, F401
print('END')
