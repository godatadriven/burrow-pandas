import json

import pandas as pd
import pytest

from burrowpandas import JsonArray


def test_if_object_can_init():
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    JsonArray(data)


def test_can_make_df(json_array):
    pd.DataFrame({'json': json_array})


def test_jsonarray_from_string(json_list):
    actual = JsonArray.from_string(json_list)
    expected = JsonArray([json.loads(json_str) for json_str in json_list])
    assert all((actual == expected) | (actual.isna() & expected.isna()))


def test_jsonarray_neq():
    assert JsonArray.from_string(['{"a": "b"}']) != JsonArray.from_string(['{"b": "b"}'])


@pytest.mark.parametrize('value', [
    ['{"a": "b"}'],
])
def test_exception_wrong_type(value):
    with pytest.raises(ValueError):
        JsonArray(value)


def test_copy():
    pass


def test_iter():
    pass


def test_merge():
    pass


def test_na_value():
    pass


def test_fillna():
    pass


def test_add_series(json_series):
    json_series.json.add(pd.Series([1, 2, 3], name='new_col'))
