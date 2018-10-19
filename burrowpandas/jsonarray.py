import json
import operator

import numpy as np
import pandas as pd
from pandas.core.arrays import ExtensionArray
from pandas.core.dtypes.base import ExtensionDtype


class Delegated:
    # Descriptor for delegating attribute access to from
    # a Series to an underlying array

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, type=None):
        index = object.__getattribute__(obj, '_index')
        name = object.__getattribute__(obj, '_name')
        result = self._get_result(obj)
        return pd.Series(result, index, name=name)


class DelegatedProperty(Delegated):
    def _get_result(self, obj, type=None):
        return getattr(object.__getattribute__(obj, '_data'), self.name)


class JsonType(ExtensionDtype):
    name = 'json'
    type = str
    kind = 'U'
    na_value = ''

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            "'{}'".format(cls, string))


class JsonArray(ExtensionArray):
    dtype = JsonType()
    can_hold_na = True
    _itemsize = 10000

    def __init__(self, values):
        self.data = values

    @classmethod
    def _from_sequence(cls, scalars):
        return cls(scalars)

    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    @property
    def shape(self):
        return (len(self.data),)

    def __len__(self):
        return len(self.data)

    @property
    def nbytes(self):
        return self._itemsize * len(self)

    def isna(self):
        return self.data == ''

    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.core.algorithms import take

        # If the ExtensionArray is backed by an ndarray, then
        # just pass that here instead of coercing to object.

        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value

        # fill value should always be translated from the scalar
        # type for the array, to the physical storage type for
        # the data, before passing to take.

        result = take(self.data, indices, fill_value=fill_value,
                      allow_fill=allow_fill)
        return self._from_sequence(result)

    def __getitem__(self, *args):
        result = operator.getitem(self.data, *args)
        return type(self)(result)

    def copy(self, deep=False):
        return type(self)(self.data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        return cls(np.concatenate([array.data for array in to_concat]))

    @property
    def keys(self):
        return [list(json.loads(json_string).keys()) for json_string in self.data]


@pd.api.extensions.register_series_accessor("json")
class JsonAccessor:

    keys = DelegatedProperty("keys")

    def __init__(self, obj):
        self._validate(obj)
        self._data = obj.values
        self._index = obj.index
        self._name = obj.name

    @staticmethod
    def _validate(obj):
        if not is_json_type(obj):
            raise AttributeError("Cannot use 'json' accessor on objects of "
                                 "dtype '{}'.".format(obj.dtype))


def is_json_type(obj):
    try:
        return isinstance(getattr(obj, 'dtype', obj), JsonType)
    except Exception:
        return False
