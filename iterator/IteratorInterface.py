from abc import ABC, abstractmethod
from typing import Any


class IteratorInterface(ABC):  # Абстрактный класс, интерфейс итератора.

    def __init__(self, collection):
        self.collection = collection

    @abstractmethod
    def next(self):
        """
        Returns:
            Next element of collection.
        """
        pass

    @abstractmethod
    def has_next(self):
        """
        Returns:
            True if collection has next element else False.
        """
        pass
