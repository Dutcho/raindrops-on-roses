"""Subpackage imports and exposes public submodules by naming in `__all__` - Olaf, 26-31 Aug 2026."""
from . import construct, dicttools, duckdb, itertools, reprtools, types

__all__ = ['construct', 'dicttools', 'duckdb', 'itertools', 'reprtools', 'types']  # explicitly list to help typecheckers

names = [name for name in globals() if not name.startswith('_')]
assert set(__all__) == set(names), f"import {names} and {__all__=} out of sync"
