# Helpers

The package provides some helpers to make the development easier.

## BaseClass

This class is used to simulate a direct comparison between python objects excluding the `id` allowing
an immediate object to object valuation.

### How to use

```python
from django_fast_utils.helpers import BaseClass


class MyObject(BaseClass):
    def __init__(self, name):
        self.name = name

obj1 = MyObject(name='test')
obj2 = MyObject(name='test')

obj1 == obj2 # returns True

```

## Slot2Object

Converts a dictionary to a python like direct object with one level.

### How to use

```python
from django_fast_utils.helpers import Slot2Object

_dict = {'a': 1, 'b': {'c': 1}, {'d': {'d1': 3}}}
s = Slot2Object(_dict)

Result:
    s.a
    1

    s.b
    {'c': 1}

```

## json_2object

Returns a Python type object from a json type

## SlotObject

Similar to [Slot2Object](#slot2object) but with access to all object levels.

Class that converts a dict into an object using slots.
Performance wise, is faster and gives a better memory usage.
This class provides a nested setattr.

### How to use

```python
from django_fast_utils.helpers import SlotObject

_dict = {'a': 1, 'b': {'c': 1}}
s = SlotObject(_dict)

Result:
    s.a
    1

    s.b.c
    1
```

## remove_prefix

For versions prior to python 3.9, removes the prefixes from a given string.

### How to use

```python
from django_fast_utils.helpers import remove_prefix

remove_prefix('mytest', 'my') # Returns 'test'

```

## Singleton

Python object implementation of a Singleton

### How to use

```python
from django_fast_utils.helpers import Singleton

class A:
    pass

class B(Singleton):
    pass

a1 = A()
a2 = A()
b1 = B()
b2 = B()

assert a1 != a2 # True
assert b1 == b2 # True

```
