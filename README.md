# Welcome!

**import-watch** allows to
trace module imports
and
detect/deny cyclic imports
*at runtime*
with Python 2 and 3.
It is licensed under the MIT license.

Enjoy!


# Installation
```console
# pip install import-watch
```


# Usage

## Trace imports
```python
import import_watch
import_watch.trace_imports(depth=2)  # default depth is unlimited
```

## Detect and warn about cyclic imports (at runtime)
```python
import import_watch
import_watch.warn_about_cyclic_imports()
```

## Deny cyclic imports (at runtime)
```python
import import_watch
import_watch.deny_cyclic_imports()
```

## Start fresh
```python
import import_watch
[..]
import_watch.reset()
```
