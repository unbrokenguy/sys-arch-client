from copy import deepcopy
from typing import List, Any

from Collection import Collection
from ArrayListIterator import ArrayListIterator


class ArrayList(Collection):

    def __init__(self, items: List[Any] = None):
        if items:
            self.items = items
        else:
            self.items = []

    def add(self, item):
        """
        Add element to collection.
        Args:
            item: element that need to add.
        """
        self.items.append(item)

    def size(self):
        """
        Returns:
            Number of element in collection.
        """
        return len(self.items)

    def remove(self, item):
        """
        Remove element from collection.
        Args:
            item: element that need to remove.
        """
        self.items.remove(item)

    def get(self, index):
        return self.items[index]

    def iterator(self):
        """
        Method to get ArrayListIterator for this ArrayList.
        Returns:
            ArrayListIterator object.
        """
        return ArrayListIterator(ArrayList(deepcopy(self.items)))
