from collections.abc import Callable
from typing import Annotated

from typing_extensions import Doc

type Endofunction[T] = Annotated[Callable[[T], T],  # TODO: propose for useful types
                                 Doc("Unary function from domain `T` to codomain `T`; "
                                     "see https://en.wikipedia.org/wiki/Endomorphism#Endofunctions.\n\n"
                                     "Definition includes many ordinary callables; "
                                     "`type` is useful to DRY for complex `T`, e.g. for decorator factories.")]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
