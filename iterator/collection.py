from collections.abc import Iterable
from typing import List, Any

from iterator.iterator import AnyIterator


class AnyCollection(Iterable):
    """
    A collection that stores items of Any type.
    """
    def __init__(self):
        self._collection: List[Any] = []

    @property
    def collection(self):
        return self._collection

    def __iter__(self) -> AnyIterator:
        """
        Returns:
            AnyIterator with direct order.
        """
        return self.get_iterator()

    def append(self, item):
        self._collection.append(item)

    def get_iterator(self, direct_order: bool = True):
        """
        Args:
            direct_order: Boolean if True return direct order iterator else reverse.
                Default value is True.
        Returns:
            AnyIterator with giver order.
        """
        return AnyIterator(collection=self.collection, direct_order=direct_order)
