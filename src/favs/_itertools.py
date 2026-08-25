"""favs.itertools - favourite iter tooling functions - Olaf, 23 Aug 2026."""
import itertools
import sys
from collections.abc import Iterable, Iterator, Sized
from typing import Iterable, overload, TYPE_CHECKING

if sys.version_info < (3, 15):
    from _types import sentinel


_NOT_GIVEN = sentinel('_NOT_GIVEN')  # sentinel for dynamic default

if TYPE_CHECKING:
    @overload
    def mark_first[T](values: Iterable[T], /) -> Iterator[tuple[T, bool]]:
        ...

    @overload
    def mark_first[T, MT](values: Iterable[T], /, *, first: MT) -> Iterator[tuple[T, MT | bool]]:
        ...

    @overload
    def mark_first[T, MT](values: Iterable[T], /, *, other: MT) -> Iterator[tuple[T, MT | bool]]:
        ...

    @overload
    def mark_first[T, MT](values: Iterable[T], /, *, first: MT, other: MT) -> Iterator[tuple[T, MT]]:
        ...


def mark_first[T, MT](values: Iterable[T], /, *, first: bool | MT = True, other: bool | MT | sentinel = _NOT_GIVEN
                      ) -> Iterator[tuple[T, bool]] | Iterator[tuple[T, MT | bool]] | Iterator[tuple[T, MT]]:
    """Iterate over `values`, each paired by a _mark_: `first` for first and `other` for succeeding others.

    Default is `True` for `first`, and `not first` for `other`.

    Similar in usage to `enumerate`, with mark `True, False, False, ...` instead of sequence number `0, 1, 2, ...`.
    Avoidance of increment and equality testing makes `mark_first` ~10% faster than `enumerate`
    (in very limited test on Windows CPython 3.12 and 3.13; **not** so on 3.14, likely due to `enumerate` optimization).

    Note combining `mark_first` and `mark_last` into single `mark` function _sounds_ logical,
    _until_ you consider `length == 1`: it would need marking as both first and last.

    >>> list(mark_first(range(4)))
    [(0, True), (1, False), (2, False), (3, False)]
    """
    if first is other:
        raise ValueError(f"cannot mark first with {first=} and {other=} because they're indistinguishable")
    if other is _NOT_GIVEN:
        other = not first  # dynamic default

    marks = itertools.chain([first], itertools.repeat(other))  # unbound
    yield from zip(values, marks)  # limited to shortest, i.e. elements


if TYPE_CHECKING:
    @overload
    def mark_last[T](values: Iterable[T], /) -> Iterator[tuple[T, bool]]:
        ...

    @overload
    def mark_last[T, MT](values: Iterable[T], /, *, last: MT) -> Iterator[tuple[T, MT | bool]]:
        ...

    @overload
    def mark_last[T, MT](values: Iterable[T], /, *, other: MT) -> Iterator[tuple[T, MT | bool]]:
        ...

    @overload
    def mark_last[T, MT](values: Iterable[T], /, *, last: MT, other: MT) -> Iterator[tuple[T, MT]]:
        ...


def mark_last[T, MT](values: Iterable[T], /, *, last: bool | MT = True, other: bool | MT | sentinel = _NOT_GIVEN
                     ) -> Iterator[tuple[T, bool]] | Iterator[tuple[T, MT | bool]] | Iterator[tuple[T, MT]]:
    """Iterate over `values`, each paired by a _mark_: `last` for last and `other` for preceding others.

    Default is `True` for `last`, and `not last` for `other`.

    Special casing for `Sized` allows speedup by ~20% (**only** in such cases) by avoidance of programmatic iteration
    (in very limited test on Windows CPython 3.12, 3.13, 3.14).

    >>> list(mark_last(range(4)))
    [(0, False), (1, False), (2, False), (3, True)]
    """
    if last is other:
        raise ValueError(f"cannot mark last with {last=} and {other=} because they're indistinguishable")
    if other is _NOT_GIVEN:
        other = not last  # dynamic default

    if isinstance(values, Sized):
        if values:                                                         # done if empty
            n = len(values) - 1                                            # fast path because known length
            marks = itertools.chain(itertools.repeat(other, n), [last])    # bound
            yield from zip(values, marks, strict=True)                     # same lengths
        return

    iterator = iter(values)                                                # slower path by element-wise iteration
    for current in iterator:
        for successor in iterator:
            yield current, other                                           # not last yet (still `successor` to go)
            current = successor
        yield current, last                                                # last


if __name__ == '__main__':
    import doctest
    doctest.testmod()
