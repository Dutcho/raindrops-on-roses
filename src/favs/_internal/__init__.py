"""Subpackage `_internal` imports public submodules and exposes them by listing in `__all__` - Olaf, 26-28 Aug 2026."""
from . import construct, dicttools, itertools, repr, types

__all__ = 'construct', 'dicttools', 'itertools', 'repr', 'types'
assert set(__all__) == {name for name in globals() if not name.startswith('_')}, "import and __all__ out of sync"
