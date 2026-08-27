"""Subpackage `_internal` imports public submodules and exposes them by listing in `__all__` - Olaf, 26 Aug 2026."""
from . import dicttools, construct, itertools, repr, types

__all__ = tuple(name for name in globals() if not name.startswith('_'))
