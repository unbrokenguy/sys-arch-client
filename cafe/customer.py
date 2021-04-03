from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class Card:
    bonuses: int = 0
    discount: float = 0.01
    total_spent: int = 0
    level: str = "silver"


@dataclass
class Customer:
    name: str
    card: Card
    email: str = ""

    def __dict__(self) -> dict:
        to_dict = {}
        to_dict.update({"name": self.name})
        to_dict.update({"card": vars(self.card)})
        to_dict.update({"email": self.email})
        return to_dict


class CardStrategy(ABC):
    card: Card

    def __init__(self, card):
        self.card = card

    @abstractmethod
    def make_discount(self, cost):
        return 0

    @abstractmethod
    def process_card(self):
        pass


class SilverCardStrategy(CardStrategy):

    def __init__(self, card):
        super().__init__(card)

    def make_discount(self, cost):
        self.card.total_spent += cost
        cost *= self.card.discount
        self.process_card()
        return cost

    def process_card(self):
        if self.card.level == "silver" and self.card.total_spent >= 10000:
            self.card.level = "gold"
            self.card.discount = 0.1


class GoldCardStrategy(CardStrategy):

    def __init__(self, card):
        super().__init__(card)

    def make_discount(self, cost):
        self.card.total_spent += cost
        self.card.bonuses += cost * self.card.discount
        cost *= self.card.discount
        return cost

    def process_card(self):
        pass
