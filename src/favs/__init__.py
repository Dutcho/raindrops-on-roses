"""Hub model for package `favs` only exposes submodules from `_internal` named in `__all__` - Olaf, 26 Aug 2026."""
if __name__ != '__main__':
    from ._internal import *

    __all__ = _internal.__all__

    del _internal

if __name__ == '__main__':
    from _internal import _doctest
