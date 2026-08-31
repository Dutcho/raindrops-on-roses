"""Hub model exposes or tests submodules from `_internal` subpackage as named in `__all__` - Olaf, 26-31 Aug 2026."""
if __name__ != '__main__':
    from ._internal import *
    __all__ = _internal.__all__
    del _internal

if __name__ == '__main__':
    from _internal import _doctest
