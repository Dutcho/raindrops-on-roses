"""favs.types - favourite types and `typing` functions - Olaf, 23-31 Aug 2026."""
from collections.abc import Callable
from typing import Annotated, Any, assert_type, cast, TYPE_CHECKING

from typing_extensions import Doc


def cast_alike[T](_exemplar: T, instance: object, /) -> T:
    """Return `instance` cast alike `_exemplar`, i.e. to type `T`.

    Equivalent to `cast(type(_exemplar), instance)`, which `mypy` 2.3.1 disapproves (though `ty` 0.0.73 allows).

    >>> n = next(iter(range(1)))    # prevent typechecker from inferring `Literal[0]`
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

    `cast_alike_callable` standardizes result type to parametrized `Callable` (for mypy),
    which `cast_alike` can't do in case of overloads.

    >>> func1 = cast_alike(ascii, lambda a, b: 0)             # lie about `func1` type/signature of simple function
    >>> assert_type(func1, Callable[[object], str])           # cannot validate at doctest runtime # doctest: +SKIP
    >>> func2 = cast_alike_callable(getattr, lambda a, b: 0)  # lie about `func2` type/signature of overloaded function
    >>> assert_type(func2, Callable[[object, str], Any])      # cannot validate at doctest runtime # doctest: +SKIP
    """
    return cast(Callable[PS, RT], instance)


if TYPE_CHECKING:
    def _test_cast_alike_callable() -> None:
        """Execute skipped doctest at typechecking time."""
        func1 = cast_alike(ascii, lambda a, b: 0)
        assert_type(func1, Callable[[object], str])           # typechecker believes lie about `func` type/signature
        func2 = cast_alike_callable(getattr, lambda a, b: 0)
        assert_type(func2, Callable[[object, str], Any])      # typechecker believes lie about `func` type/signature


type EndoFunction[T] = Annotated[Callable[[T], T],
                                 Doc("Single-argument function with same domain and co-domain.")]


if TYPE_CHECKING:
    def _test_endo_function() -> None:
        """Execute doctest equivalent at typechecking time."""
        def test[T](_: EndoFunction[T], /) -> None: pass  # only accepts `EndoFunction`
        def func(_: int, /) -> int: return False          # (int) -> int, i.e. `EndoFunction`
        test(func)
