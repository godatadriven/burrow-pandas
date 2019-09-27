import json

import numpy as np
import pandas as pd
import pyjq

from burrowpandas.base import NumPyBackedExtensionArrayMixin
from burrowpandas.delegated import delegated_method, DelegatedProperty, DelegatedMethod
from pandas.api.extensions import ExtensionDtype, take


# @register_extension_dtype from pandas 0.24
class JsonType(ExtensionDtype):
    name = 'json'
    type = object
    kind = 'O'
    _record_type = np.dtype('O')
    na_value = {}

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            ""'{}'"".format(cls, string))


class JsonArray(NumPyBackedExtensionArrayMixin):
    _dtype = JsonType()
    can_hold_na = True
    _itemsize = 10000

    def __init__(self, values):
        supported_types = (dict, list)
        if not all(isinstance(val, supported_types) for val in values):
            wrong_type = [type(val) for val in values if  not isinstance(val, supported_types)]
            raise ValueError("Cannot construct a JsonArray from '{}'".format(wrong_type))
        self.data = np.array(values)

    @classmethod
    def from_string(cls, values, *args, **kwargs):
        # todo: vectorize json load
        return cls(np.array([json.loads(j, *args, **kwargs) for j in values]))

    @property
    def keys(self):
        """Returns a list of top-level keys for each item in the series0"""
        return [list(d.keys()) for d in self.data]

    @property
    def size(self):
        return len(self.data)

    @property
    def na_value(self):
        return self.dtype.na_value

    def take(self, indexer, allow_fill=False, fill_value=None):
        if fill_value is None:
            fill_value = 0
        took = take(self.data, indexer, allow_fill=allow_fill,
                    fill_value=fill_value)
        return type(self)(took)

    def has_key(self, key):
        """Returns a boolean indicating whether the key is present in the json text"""
        return [key in keys for keys in self.keys]

    def update(self, dct):
        return type(self)(pyjq.first('map(. + {})'.format(json.dumps(dct)), list(self.data)))

    def filter(self, jq_string):
        return type(self)(pyjq.all('.[] | ' + jq_string, list(self.data)))

    def isna(self):
        return self.data == self.na_value

    def _format_values(self):
        return self.data

    def __repr__(self):
        formatted = self._format_values()
        return 'JsonArray({!r})'.format(formatted)

    def __iter__(self):
        return iter(self.data)

    def add(self, other):
        other_data = [{other.name: datum} for datum in other.data]
        return type(self)(
            pyjq.all('[.] + [{}] | transpose | map(add)'.format(json.dumps(other_data)), list(self.data))[0]
        )

    def __eq__(self, other):
        if not isinstance(other, JsonArray):
            return NotImplemented
        mask = self.isna() | other.isna()
        result = self.data == other.data
        result[mask] = False
        return result

    def __ne__(self, other):
        return ~self.__eq__(other)


@pd.api.extensions.register_series_accessor('json')
class JsonAccessor:

    keys = DelegatedProperty('keys')
    isna = DelegatedMethod('isna')
    
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

    def has_key(self, key):
        return delegated_method(self._data.has_key, self._index,
                                self._name, key)

    def update(self, dct):
        return delegated_method(self._data.update, self._index,
                                self._name, dct)

    def add(self, dct):
        return delegated_method(self._data.add, self._index,
                                self._name, dct)


@pd.api.extensions.register_series_accessor('jq')
class JQAccessor:
    def __init__(self, obj):
        self._validate(obj)
        self._data = obj.values
        self._index = obj.index
        self._name = obj.name

    @staticmethod
    def _validate(obj):
        if not is_json_type(obj):
            raise AttributeError("Cannot use 'jq' accessor on objects of "
                                 "dtype '{}'.".format(obj.dtype))

    def filter(self, jq_string):
        return delegated_method(self._data.filter, self._index,
                                self._name, jq_string)

    def explode(self, jq_string):

        data = [{**{'__index__': int(index)}, **datum} for datum, index in zip(self._data.data, list(self._index.values))]
        result = pyjq.all('.[] | {__index__: .__index__, ' + jq_string[1:], list(data))
        new_index = [res.pop('__index__') for res in result]

        return pd.Series(JsonArray(result), new_index, name=self._name)


def is_json_type(obj):
    try:
        return isinstance(getattr(obj, 'dtype', obj), JsonType)
    except Exception:
        return False
