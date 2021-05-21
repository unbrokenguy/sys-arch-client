from abc import ABC, abstractmethod


class Collection(ABC):

    @abstractmethod
    def add(self, item):
        """
        Add element to collection.
        Args:
            item: element that need to add.
        """
        pass

    @abstractmethod
    def size(self):
        """
        Returns:
            Number of element in collection.
        """
        pass

    @abstractmethod
    def remove(self, item):
        """
        Remove element from collection.
        Args:
            item: element that need to remove.
        """
        pass

    @abstractmethod
    def iterator(self):
        """
        Get Iterator for this collection.
        Returns:
            IteratorInterface
        """
        pass
