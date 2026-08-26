print("at __init__", __file__)
try:
    from . import _dicttools as dicttools
    from . import _itertools as itertools
    from . import _repr as repr
    from . import _types as types
    print("imported from .")
except ImportError as exc:
    print(repr(exc))
    import _dicttools
    import _itertools
    import _repr
    import _types
    print("imported _")

if __name__ == '__main__':
    import doctest
    doctest.testmod(_dicttools)
    doctest.testmod(_itertools)
    doctest.testmod(_repr)
    doctest.testmod(_types)
