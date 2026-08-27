from collections.abc import Callable
from typing import Any, assert_type, cast, overload, TYPE_CHECKING

from typing_extensions import TypeForm


@overload
def cast_alike_callable[**PS, RT](func_type: TypeForm[Callable[PS, RT]], value: object, /) -> Callable[PS, RT]:
    """Return `value` cast to `func_type`, i.e. to same type and signature."""


@overload
def cast_alike_callable[**PS, RT](func: Callable[PS, RT], value: object, /) -> Callable[PS, RT]:
    """Return `value` cast alike callable `func`, i.e. to same type and signature."""


def cast_alike_callable[**PS, RT](_arg: Callable[PS, RT] | TypeForm[Callable[PS, RT]], value: object, /
                                  ) -> Callable[PS, RT]:
    """Return `value` cast alike callable `func` (or to `func_type` if `TypeForm`), i.e. to same type and signature.

    >>> f = cast_alike_callable(getattr, lambda *args: 0)       # lie to typechecker about signature
    >>> assert_type(f, Callable[[object, str], Any])            # cannot validate at runtime # doctest: +SKIP
    """
    if TYPE_CHECKING:
        getattr_type = Callable[[object, str], Any]
        f = cast_alike_callable(getattr, lambda *args: 0)       # redo doctest at typechecking time
        assert_type(f, getattr_type)                            # typechecker believes lie about f
        g = cast_alike_callable(getattr_type, lambda *args: 0)  # typeform test at typechecking time
        assert_type(g, getattr_type)                            # typechecker believes lie about f

    return cast(Callable[PS, RT], value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
