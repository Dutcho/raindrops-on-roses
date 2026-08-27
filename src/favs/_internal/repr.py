"""favs.repr - favourite string representation functions - Olaf, 23 Aug 2026."""
import inspect
import itertools
from collections.abc import Callable
from inspect import Signature
from typing import assert_never, Final, Literal, Annotated

from typing_extensions import Doc


type _SignaturePartName = Annotated[Literal['parameters', 'return_annotation'],
                                    Doc("Literal name of one of two parts of signature.")]


def function_repr(function: Callable[..., object], /) -> str:
    """Return string representation of `function` identifier incl. its module name if not 'trivial'.

    >>> function_repr(function_repr)  # doctest: +ELLIPSIS
    '...function_repr'
    """
    trivial = {'__main__', 'buildins', None}
    module_name = function.__module__
    return '.'.join(itertools.chain([] if module_name in trivial else [module_name],
                                    [function.__qualname__]))


def _empty_signature(signature: Signature, *args: _SignaturePartName) -> Signature:
    """Return `signature` with `*args` parts emptied."""
    _EMPTY: Final = inspect.Signature.empty
    for empty in args:
        match empty:
            case 'parameters':
                params = signature.parameters.values()
                empty_params = [param.replace(annotation=_EMPTY) for param in params]
                signature = signature.replace(parameters=empty_params)
            case 'return_annotation':
                signature = signature.replace(return_annotation=_EMPTY)
            case _:
                assert_never(empty)
    return signature


def _function_empty_signature(function: Callable[..., object], *args: _SignaturePartName) -> str:
    """Return string representation of `function` identifier, followed by signature with `*args` parts emptied."""
    signature = _empty_signature(inspect.signature(function), *args)
    return f'{function_repr(function)}{signature}'


def function_call_repr(function: Callable[..., object], /) -> str: # f(a)
    """Return string representation of `function` call incl. its parameter names.

    >>> function_call_repr(function_call_repr)  # doctest: +ELLIPSIS
    '...function_call_repr(function, /)'
    """
    return _function_empty_signature(function, 'parameters', 'return_annotation')


def function_param_repr(function: Callable[..., object], /) -> str: # f(a: int)
    """Return string representation of `function` incl. its parameters with their signature.

    >>> function_param_repr(function_param_repr)  # doctest: +ELLIPSIS
    '...function_param_repr(function: ...Callable[..., object], /)'
    """
    return _function_empty_signature(function, 'return_annotation')


def function_signature_repr(function: Callable[..., object], /) -> str: # f(a: int) -> str
    """Return string representation of `function` incl. its full signature.

    >>> function_signature_repr(function_signature_repr)  # doctest: +ELLIPSIS
    '...function_signature_repr(function: ...Callable[..., object], /) -> str'
    """
    return _function_empty_signature(function)


def function_header_repr(function: Callable[..., object], /) -> str:  # def f(a: int) -> str
    """Return string representation of `function` as its definition header line.

    >>> function_header_repr(function_header_repr)  # doctest: +ELLIPSIS
    'def ...function_header_repr(function: ...Callable[..., object], /) -> str'
    """
    return f'def {function_signature_repr(function)}'


def args_kwargs_repr(*args: object, **kwargs: object) -> str:
    """Return comma-separated string representation of `*args` (as `repr`) and `**kwargs` (as `'{}={!r}'`).

    >>> args_kwargs_repr(1, 'two', 3, x=24, y='why', z=26)
    "1, 'two', 3, x=24, y='why', z=26"
    """
    sep, arg_repr, kwarg_repr = ', ', repr, '{}={!r}'.format

    args_repr = map(arg_repr, args)
    kwargs_repr = map(kwarg_repr, kwargs.keys(), kwargs.values())
    return sep.join(itertools.chain(args_repr, kwargs_repr))


def call_repr(function: Callable[..., object], *args: object, **kwargs: object) -> str:
    """Return string representation of `function` call incl. its `*args` and `**kwargs`.

    >>> call_repr(call_repr, call_repr)  # doctest: +ELLIPSIS
    '...call_repr(<function call_repr...>)'
    """
    return f'{function_repr(function)}({args_kwargs_repr(*args, **kwargs)})'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
