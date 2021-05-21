from IteratorInterface import IteratorInterface


class ArrayListIterator(IteratorInterface):

    def __init__(self, array_list):
        if array_list.__class__.__name__ != "ArrayList":
            raise TypeError
        super().__init__(array_list)
        self.index = 0

    def next(self):
        """
         Returns:
             Next element of collection.
         """
        try:
            value = self.collection.get(self.index)
            self.index += 1
            return value
        except IndexError:
            raise StopIteration

    def has_next(self):
        """
        Returns:
            True if collection has next element else False.
        """
        try:
            self.collection.get(self.index)
            return True
        except IndexError:
            return False
