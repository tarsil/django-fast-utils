import datetime
import pytz
import json
from collections import namedtuple
import functools


class BaseClass:
    """
    This class serves with the purpose of dynamically create a constructor and override the default
    __eq__ operator from python allowing the direct comparison between python objects
    """

    def __init__(self, **kwargs):
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __eq__(self, instance):
        if not isinstance(instance, self.__class__):
            return False
        if hash(frozenset(self.__dict__.items())) == hash(frozenset(instance.__dict__.items())):
            return True
        return False

    def __ne__(self, instance):
        if not isinstance(instance, self.__class__):
            return True
        if hash(frozenset(self.__dict__.items())) != hash(frozenset(instance.__dict__.items())):
            return True
        return False

    @property
    def utc(self):
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        return utc_now

    def __repr__(self):
        return '<%s - %s />' % (self.__class__.__name__, self.utc)


class Slot2Object:
    """
    Class that converts a dict into a object using slots.
    Performance wise, is faster and gives a better memory usage.

    Usage:
    _dict = {'a': 1, 'b': {'c': 1}}
    s = Slot2Object(_dict)

    Result:
        s.a
        1

        s.b
        {'c': 1}
    """
    __slots__ = ['__dict__']

    def __init__(self, __dict__):
        self.__dict__ = __dict__

    def __getitem__(self, item):
        return getattr(self, item)


def json_2object(json_payload):
    """
    Returns a Python type object from a json type
    :param json_payload: Json to be converted
    :return: Python object
    """
    return json.loads(json_payload, object_hook=lambda d: namedtuple('X', list(d.keys()))(*list(d.values())))


def rgetattr(obj, attr, *args): # pragma: no cover
    """
    A replacement of the default getattr() with a nuance of getting the nested values from objects
    :param obj: Object to lookup
    :param attr: Attribute to search
    :param args: Defaut value
    :return: Value
    """

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))


class SlotObject:
    """
    Class that converts a dict into an object using slots.
    Performance wise, is faster and gives a better memory usage.
    This class provides a nested setattr.

    Usage:
        _dict = {'a': 1, 'b': {'c': 1}}
        s = SlotObject(_dict)

    Result:
        s.a
        1

        s.b.c
        1
    """
    __slots__ = ['__dict__']

    def __init__(self, __dict__):
        for k, v in __dict__.items():
            setattr(
                self, k, self.__class__(v)) if isinstance(v, dict) and v else setattr(self, k, v)

    def __getitem__(self, item):
        return getattr(self, item)


def remove_prefix(text, prefix):
    """
    In python 3.9 there is already a native function to remove the prefixes.
    See https://www.python.org/dev/peps/pep-0616/
    If the version is inferior to 3.9 then runs the below solution.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


class Singleton:
    """
    Simple python object representation of a Singleton.
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is not None:
            return cls.instance

        _instance = cls.instance = super().__new__(cls, *args, **kwargs)
        return _instance