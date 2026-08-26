"""favs.dicttools - favourite dict/Mapping tooling functions - Olaf, 23 Aug 2026."""
from collections.abc import Callable, Iterable, Mapping
from typing import cast, overload, TYPE_CHECKING

from ._types import Endofunction


if TYPE_CHECKING:
    @overload
    def _mapping_as_cls[KT1, VT1, KT, VT](cls: type[Mapping[KT1, VT1]], mapping: Mapping[KT, VT], /
                                          ) -> Mapping[KT, VT]: ...

    @overload
    def _mapping_as_cls[KT1, VT1, KT, VT](cls: type[Mapping[KT1, VT1]], kv_pairs: Iterable[tuple[KT, VT]], /
                                          ) -> Mapping[KT, VT]: ...

    @overload
    def _mapping_as_cls[KT1, VT1, KT, VT](cls: type[Mapping[KT1, VT1]], keys: Iterable[KT], values: Iterable[VT], /
                                          ) -> Mapping[KT, VT]: ...


def _mapping_as_cls[KT1, VT1, KT, VT](cls: type[Mapping[KT1, VT1]], /, *args: object) -> Mapping[KT, VT]:
    """Return `*args` converted to type `cls` at runtime, respecting `[KT, VT]` generics of `*args` when typechecking.

    >>> from collections import OrderedDict
    >>> _mapping_as_cls(OrderedDict, {'a': 1, 'b': 2})
    OrderedDict({'a': 1, 'b': 2})
    >>> from typing import reveal_type
    >>> reveal_type(_mapping_as_cls(OrderedDict, {'a': 1, 'b': 2}))  # cannot test typechecking # doctest: +SKIP
    Revealed type is "typing.Mapping[str, int]"
    """
    match args:
        case [Mapping() as mapping]:  # overload 1
            pass
        case [Iterable() as kv_pairs]:  # overload 2
            mapping = dict(kv_pairs)
        case [Iterable() as keys, Iterable() as values]:  # overload 3
            mapping = dict(zip(keys, values, strict=True))
        case _:
            raise TypeError(f"{args!r} do not match any @overload of {_mapping_as_cls}")

    mapping_kt_vt = cast(Endofunction[Mapping[KT, VT]], cast(object, cls))  # `Mapping[KT, VT]` with origin of `cls`
    return mapping_kt_vt(mapping)  # values as get_origin(cls)[KT, VT]


def map_mapping_keys[KT, VT, RT](transform: Callable[[KT], RT], mapping: Mapping[KT, VT], /) -> Mapping[RT, VT]:
    """Return `mapping` with `transform`ed `keys()`, failing if multiple keys get mapped to same value.

    Result preserves `mapping`'s runtime type, with `[RT, VT]` generics for `Mapping` at typechecking time.

    >>> map_mapping_keys(str, {1: 1, 2: 2})
    {'1': 1, '2': 2}
    """
    transformed_keys = list(map(transform, mapping.keys()))
    if len(transformed_keys) != len(mapping):  # unique keys transformed to non-unique ones, i.e. collision
        raise ValueError(f"{transform} cannot map keys; overlap gives "
                         f"result {len(transformed_keys)=} != original {len(mapping)=}")
    return _mapping_as_cls(type(mapping), transformed_keys, mapping.values())


def map_mapping_values[KT, VT, RT](transform: Callable[[VT], RT], mapping: Mapping[KT, VT], /) -> Mapping[KT, RT]:
    """Return `mapping` with `transform`ed `values()`.

    Result preserves `mapping`'s runtime type, with `[KT, RT]` generics for `Mapping` at typechecking time.

    >>> map_mapping_values(str, {1: 1, 2: 2})
    {1: '1', 2: '2'}
    """
    transformed_values = map(transform, mapping.values())
    return _mapping_as_cls(type(mapping), mapping.keys(), transformed_values)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
