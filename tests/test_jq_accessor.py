import pandas as pd

from burrowpandas import JsonArray
from burrowpandas.jsonarray import JQAccessor


def test_jq_accessor_registered(json_series):
    assert type(json_series.jq) == JQAccessor


def test_jq_filter(json_series):
    result = pd.Series(JsonArray([
        {'age': 29, 'name': 'Molecule Man'},
        {'age': 39, 'name': 'Madame Uppercut'},
        {'age': None, 'name': None},
    ]))
    assert all(json_series.jq.filter('{age: .age, name: .name}') == result)


def test_explode(json_series):
    json_series.jq.explode('{name: .name?, power: .powers[]?}')