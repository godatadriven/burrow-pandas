import pandas as pd
import pytest

from burrowpandas import JsonArray


@pytest.fixture
def json_list():
    return [
    '''{
    "name": "Molecule Man",
    "age": 29,
    "secretIdentity": "Dan Jukes",
    "powers": [
        "Radiation resistance",
        "Turning tiny",
        "Radiation blast"
    ]
    }
    ''',
    '''
    {
     "name": "Madame Uppercut",
     "age": 39,
     "secretIdentity": "Jane Wilson",
     "powers": [
        "Million tonne punch",
        "Damage resistance",
        "Superhuman reflexes"
     ]
    }
    ''',
    '{}']

@pytest.fixture
def json_array(json_list):
    return JsonArray.from_string(json_list)


@pytest.fixture
def json_series(json_array):
    return pd.Series(json_array)