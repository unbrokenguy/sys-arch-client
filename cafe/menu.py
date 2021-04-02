from dataclasses import dataclass
from typing import List


@dataclass
class MenuEntry:
    name: str
    cost: int
    ingredients: List[str]


class MozzarellaPizza(MenuEntry):
    def __init__(self):
        super().__init__(
            name=self.__class__.__name__,
            cost=499,
            ingredients=["Milk", "Mozzarella", "Citric Acid", "Cheese Salt", "Rennet Tablet"],
        )


class Borscht(MenuEntry):
    def __init__(self):
        super().__init__(
            name=self.__class__.__name__, cost=249, ingredients=["Beef", "Water", "Salt", "Beets", "Onion"]
        )


class Tea(MenuEntry):
    def __init__(self):
        super().__init__(name=self.__class__.__name__, cost=50, ingredients=["Water", "Ceylon tea"])
