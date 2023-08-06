import inspect
from enum import Enum

from typing import Collection, Tuple, Optional, Any, T, KT, VT, Dict, Union, Type


def hasargs(type_, *args):
    try:
        if not type_.__args__:
            return False
        res = all(arg in type_.__args__ for arg in args)
    except AttributeError:
        return False
    else:
        return res


def issubclass_safe(cls, classinfo):
    try:
        result = issubclass(cls, classinfo)
    except Exception:
        return cls is classinfo
    else:
        return result


def is_tuple(type_) -> bool:
    try:
        # __origin__ exists in 3.7 on user defined generics
        return issubclass_safe(type_.__origin__, Tuple) or issubclass_safe(type_, Tuple)
    except AttributeError:
        return False


def is_collection(type_) -> bool:
    try:
        # __origin__ exists in 3.7 on user defined generics
        return issubclass_safe(type_.__origin__, Collection) or issubclass_safe(type_, Collection)
    except AttributeError:
        return False


def is_optional(type_) -> bool:
    return issubclass_safe(type_, Optional)


def is_union(type_: Type) -> bool:
    try:
        return issubclass_safe(type_.__origin__, Union)
    except AttributeError:
        return False


def is_any(type_: Type) -> bool:
    return type_ in (Any, T, KT, VT, inspect._empty)


def is_none(type_: Type) -> bool:
    return type_ is type(None)


def is_enum(cls: Type) -> bool:
    return issubclass_safe(cls, Enum)


def is_dict(cls):
    try:
        origin = cls.__origin__ or cls
        return origin in (dict, Dict)
    except AttributeError:
        return False
