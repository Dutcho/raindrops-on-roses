import inspect
from collections.abc import Callable, Container, Iterator, Mapping
from types import CodeType, FunctionType
from typing import Final

_EMPTY: Final = inspect.Parameter.empty
_POS_PARAM_KINDS: Final = {inspect._ParameterKind.POSITIONAL_ONLY, inspect._ParameterKind.POSITIONAL_OR_KEYWORD}
_KW_PARAM_KINDS: Final = {inspect._ParameterKind.KEYWORD_ONLY}


def _dummy(a, *args: object, b, **kwargs: object) -> None:
    print(a, args, b, kwargs)


def _signature_properties(prop: property, signature: inspect.Signature,
                          kinds: Container[inspect._ParameterKind]) -> Mapping[str, object]:
    """Return mapping {parameter name -> property value} for property `prop` of `kinds` parameters in `signature`."""
    def pairs() -> Iterator[tuple[str, object]]:
        """Iterate over (name, property value) tuples for property `prop` of `kinds` parameters in `signature`."""
        for param in signature.parameters.values():
            if param.kind in kinds:
                if prop.fget(param) is not _EMPTY:
                    yield param.name, prop.fget(param)

    return dict(pairs())


def _signature_annotations(signature: inspect.Signature,
                           kinds: Container[inspect._ParameterKind] = inspect._ParameterKind) -> Mapping[str, object]:
    """Return mapping {parameter name -> annotation} for `kinds` parameters (default all) in `signature`."""
    return _signature_properties(inspect.Parameter.annotation, signature, kinds)


def _signature_defaults(signature: inspect.Signature,
                        kinds: Container[inspect._ParameterKind] = inspect._ParameterKind) -> Mapping[str, object]:
    """Return mapping {parameter name -> default} for `kinds` parameters (default all) in `signature`."""
    return _signature_properties(inspect.Parameter.default, signature, kinds)


def construct_code(signature: inspect.Signature, name: str | None = None) -> CodeType:
    """Return function code with name `name` and signature `signature`."""
    def code_obj(
            argcount: int,
            posonlyargcount: int,
            kwonlyargcount: int,
            nlocals: int,
            stacksize: int,
            flags: int,
            codestring: bytes,
            constants: tuple[object, ...],
            names: tuple[str, ...],
            varnames: tuple[str, ...],
            filename: str,
            name: str,
            qualname: str,
            firstlineno: int,
            linetable: bytes,
            exceptiontable: bytes,
            freevars: tuple[str, ...] = ...,
            cellvars: tuple[str, ...] = ...,
            /,
    ) -> CodeType: ...

    code = _dummy.__code__ or code_obj()
    print(code.co_argcount,)
    return code


def construct_function[**PS, RT](signature: inspect.Signature, name: str | None = None) -> Callable[PS, RT]:
    """Return function with name `name` and signature `signature`."""
    function = FunctionType(code=construct_code(signature, name),
                            globals=dict[str, object](),
                            name=name,
                            argdefs=tuple(_signature_defaults(signature, _POS_PARAM_KINDS).values()) or None,
                            closure=None,
                            kwdefaults=dict(_signature_defaults(signature, _KW_PARAM_KINDS)) or None,
                            )
    function.__annotations__ = dict(_signature_annotations(signature)) | ({'return': signature.return_annotation}
                                                                          if signature.return_annotation is not _EMPTY
                                                                          else {})
    return function


def test():
    def f(a: int = 42, /, *, b=3.14, c: float) :
        return a + b + c

    s = inspect.signature(f)
    new = construct_function(s, 'test')
    help(new)
    print(new.__annotations__)


if __name__ == '__main__':
    test()
