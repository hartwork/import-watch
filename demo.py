# Copyright (C) 2019 Sebastian Pipping <sebastian@pipping.org>
# Licensed under the MIT license

from __future__ import print_function

import import_spy


print('BEGIN')
import_spy.report_on_imports(depth=1)
import yaml  # noqa: E402
import yaml  # noqa: E402, F811
import_spy.reset()
print('END')
print()


import yaml  # noqa: E402, F811


print('BEGIN')
import_spy.deny_cyclic_imports()
try:
    from cyclic_import_package import a
except ImportError as e:
    print('Exception caught:', e)
else:
    assert False, 'Cyclic import went undetected'
import_spy.reset()
print('END')
print()


import yaml  # noqa: E402, F401, F811


print('BEGIN')
import_spy.warn_about_cycle_imports()
from cyclic_import_package import a  # noqa: E402, F401, F811
import_spy.reset()
print('END')
