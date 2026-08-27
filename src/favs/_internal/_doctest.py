import doctest
from . import *
from . import __all__
names = __all__
print(names)
modules = dicttools, itertools, repr, types
for m in modules:
    doctest.testmod(m)
