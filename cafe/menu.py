from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class MenuEntry(ABC):
    """Menu Entry abstract class.

    DataClass with __init__, __eq__ and __repr__ methods that built in.

    Attributes:
        name: A string representing name of the dish.
        cost: An integer cost of the dish.
        ingredients: A list of strings with name of ingredients.
    """
    name: str
    cost: int
    ingredients: List[str]


class MozzarellaPizza(MenuEntry):
    """Implementation of MenuEntry.

    Class that represents MozzarellaPizza.
    """
    def __init__(self):
        super().__init__(
            name=self.__class__.__name__,
            cost=499,
            ingredients=["Milk", "Mozzarella", "Citric Acid", "Cheese Salt", "Rennet Tablet"],
        )


class Borscht(MenuEntry):
    """Implementation of MenuEntry.

    Class that represents Borscht.
    """
    def __init__(self):
        super().__init__(
            name=self.__class__.__name__, cost=249, ingredients=["Beef", "Water", "Salt", "Beets", "Onion"]
        )


class Tea(MenuEntry):
    """Implementation of MenuEntry.

    Class that represents Tea.
    """
    def __init__(self):
        super().__init__(name=self.__class__.__name__, cost=50, ingredients=["Water", "Ceylon tea"])
