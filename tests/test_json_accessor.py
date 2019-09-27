import pandas as pd

from burrowpandas.jsonarray import JsonAccessor


def test_json_accessor_registered(json_series):
    assert type(json_series.json) == JsonAccessor


def test_json_keys(json_series):
    assert list(json_series.json.keys) == [
        ['name', 'age', 'secretIdentity', 'powers'],
        ['name', 'age', 'secretIdentity', 'powers'],
        []
    ]


def test_isna(json_series):
    assert all(json_series.isna() == pd.Series([False, False, True]))


def test_has_key(json_series):
    assert all(json_series.json.has_key('name') | json_series.isna())
    assert not any(json_series.json.has_key('invalid_key'))


def test_update(json_series):
    result = json_series.json.update({'test': 'value'})
    assert all(result.json.has_key('test'))