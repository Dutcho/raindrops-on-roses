import sys
from collections.abc import Callable
from typing import Annotated, LiteralString

from typing_extensions import Doc

type Endofunction[T] = Annotated[Callable[[T], T],  # TODO: propose for useful types
                                 Doc("Unary function from domain `T` to codomain `T`; "
                                     "see https://en.wikipedia.org/wiki/Endomorphism#Endofunctions.\n\n"
                                     "Definition includes many ordinary callables; "
                                     "`type` is useful to DRY for complex `T`, e.g. for decorator factories.")]

if sys.version_info < (3, 15):
    class sentinel:
        """Placeholder `sentinel` until it becomes builtin in Python 3.15."""
        def __init__(self, _name: LiteralString, /) -> None:
            pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
