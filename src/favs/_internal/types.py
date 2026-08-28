from collections.abc import Callable
from typing import assert_type, cast, TYPE_CHECKING


def cast_alike[T](_exemplar: T, instance: object, /) -> T:
    """Return `instance` cast alike `_exemplar`, i.e. to type `T`.

    Equivalent to `cast(type(_exemplar), instance)`, which `mypy` 2.3.1 disapproves (though `ty` 0.0.73 allows).

    >>> n = next(iter(range(1)))    # prevent typechecker from inferring `Literal`
    >>> obj = cast_alike(n, 'abc')  # lie about `obj` type to typechecker
    >>> assert_type(obj, int)       # cannot validate at doctest runtime # doctest: +SKIP
    """
    return cast(T, instance)


if TYPE_CHECKING:
    def _test_cast_alike() -> None:
        """Execute skipped doctest at typechecking time."""
        n = next(iter(range(1)))
        obj = cast_alike(n, 'abc')
        assert_type(obj, int)       # typechecker believes lie about `obj` type


def cast_alike_callable[**PS, RT](_exemplar: Callable[PS, RT], instance: object, /) -> Callable[PS, RT]:
    """Return `instance` cast alike callable `_exemplar`, i.e. to same type and signature `Callable[PS, RT]`.

    `cast_alike_callable` standardizes result type to parametrized `Callable` (for mypy), which `cast_alike` can't.

    >>> func = cast_alike_callable(ascii, lambda a, b: 0)  # lie about `func` type and signature to typechecker
    >>> assert_type(func, Callable[[object], str])         # cannot validate at doctest runtime # doctest: +SKIP
    """
    return cast(Callable[PS, RT], instance)


if TYPE_CHECKING:
    def _test_cast_alike_callable() -> None:
        """Execute skipped doctest at typechecking time."""
        func = cast_alike_callable(ascii, lambda a, b: 0)
        assert_type(func, Callable[[object], str])         # typechecker believes lie about `func` type and signature


if __name__ == '__main__':
    import doctest
    doctest.testmod()
