import doctest
import sys

from . import __all__


def test() -> None:
    *parents, _ = __name__.split('.')
    names = ['.'.join([*parents, name]) for name in __all__]
    modules = [sys.modules[name] for name in names]

    for module in modules:
        doctest.testmod(module)


test()
