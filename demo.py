# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function

import import_watch


print('BEGIN')
import_watch.report_on_imports(depth=2)
import yaml  # noqa: E402
import yaml  # noqa: E402, F811
import_watch.reset()
print('END')
print()


import yaml  # noqa: E402, F811


print('BEGIN')
import_watch.deny_cyclic_imports()
try:
    from import_watch._cyclic_import_package import a
except ImportError as e:
    print('Exception caught:', e)
else:
    assert False, 'Cyclic import went undetected'
import_watch.reset()
print('END')
print()


import yaml  # noqa: E402, F401, F811


print('BEGIN')
import_watch.warn_about_cycle_imports()
from import_watch._cyclic_import_package import a  # noqa: E402, F401, F811
import_watch.reset()
print('END')
