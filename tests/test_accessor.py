import pandas as pd

from burrowpandas import JsonAccessor


def test_can_make_df(json_array):
    pd.DataFrame({'json': json_array})


def test_json_accessor_registered(json_series):
    assert type(json_series.json) == JsonAccessor


def test_json_keys(json_series):
    assert list(json_series.json.keys) == [
        ['name', 'age', 'secretIdentity', 'powers'],
        ['name', 'age', 'secretIdentity', 'powers']
    ]
