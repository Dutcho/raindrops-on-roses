"""Execute `doctest`s in submodules in subpackage as named in `__all__` - Olaf, 31 Aug 2026."""
import doctest
import sys
from types import ModuleType

from . import __all__


def sibling_modules() -> list[ModuleType]:
    """Return `__all__` modules that as sibling to this module."""
    *parents, _ = __name__.split('.')
    names = ['.'.join([*parents, name]) for name in __all__]
    return [sys.modules[name] for name in names]


def execute_all_doctests() -> None:
    """Execute `doctest`s in `__all__` sibling submodules."""
    for module in sibling_modules():
        doctest.testmod(module)


execute_all_doctests()
