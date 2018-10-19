from .base import NumPyBackedExtensionArrayMixin


class NestedArray(NumPyBackedExtensionArrayMixin):
    """Holder for Nested Data Structures
    IPArray is a container for IPv4 or IPv6 addresses. It satisfies pandas'
    extension array interface, and so can be stored inside
    :class:`pandas.Series` and :class:`pandas.DataFrame`.
    See :ref:`usage` for more.
    """
    def __init__(self, data):
        self.data = data