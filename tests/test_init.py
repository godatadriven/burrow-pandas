from burrowpandas import NestedArray


def test_if_object_can_init():
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    NestedArray(data)
