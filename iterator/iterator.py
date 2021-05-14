from typing import Any
from collections.abc import Iterator


class AnyIterator(Iterator):
    """
    Iterator of AnyCollection
    Attributes:
        _collection: AnyCollection object.
        _index: Next element position.
        _order: 1 if direct order, 0 if reverse order.
    """
    def __init__(self, collection, direct_order: bool):
        """
        Initialize Iterator
        Args:
            collection: AnyCollection object.
        """
        self._collection = collection
        self._index = 0 if direct_order else -1
        self._order = 1 if direct_order else -1

    def __next__(self) -> Any:
        """
        Return next collection item.
        Returns:
            Next element.
        Raises:
            StopIteration when no next element.
        """
        try:
            value = self._collection[self._index]
            self._index += self._order
            return value
        except IndexError:
            raise StopIteration()

    def next(self) -> Any:
        return self.__next__()

