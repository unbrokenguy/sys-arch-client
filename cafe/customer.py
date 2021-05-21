from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class Card:
    """Card class.

    Card always participates in the purchase process.
    Card always begins as Silver.
    Gold card has discount 0.1 and bonuses
    Silver card can be Gold only after 10000 total spent.

    DataClass with __init__, __eq__ and __repr__ methods that built in.

    Attributes:
        bonuses: An integer sum of bonuses.
        discount: A float with discount value.
        total_spent: A integer sum of all spent money.
        level: An String - level of card, can be only silver or gold.
               """
    bonuses: int = 0
    discount: float = 0.01
    total_spent: int = 0
    level: str = "silver"


@dataclass
class Customer:
    """Card class.

    DataClass with __init__, __eq__ and __repr__ methods that built in.

    Attributes:
        name: A string with customer name.
        card: A Card that customer has.
        email: An string with customer email.
    """
    name: str
    card: Card
    email: str = ""

    def __dict__(self) -> dict:
        """Return Customer object in dict format.

        Returns:
            dict: A dictionary with all data about customer and card.
        """
        to_dict = {}
        to_dict.update({"name": self.name})
        to_dict.update({"card": vars(self.card)})
        to_dict.update({"email": self.email})
        return to_dict


class CardStrategy(ABC):
    """Abstract Card Strategy

    Attributes:
        card: A Card that customer has.
    Methods:
        make_discount: Function makes discount from price.
        process_card: Function that process card.
    """
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
        """Function that makes discount, and processing card.

        Args:
            cost: An integer cost.

        Returns:
            Integer that represent discount.
        """
        self.card.total_spent += cost
        cost *= self.card.discount
        self.process_card()
        return cost

    def process_card(self):
        """Process card.
        If card level is silver and total spent greater 10000, makes card level gold.
        """
        if self.card.level == "silver" and self.card.total_spent > 10000:
            self.card.level = "gold"
            self.card.discount = 0.1


class GoldCardStrategy(CardStrategy):

    def __init__(self, card):
        super().__init__(card)

    def make_discount(self, cost):
        """Function that makes discount, and add bonuses to a card.

        Args:
            cost: An integer cost.

        Returns:
            Integer that represent discount.
        """
        self.card.total_spent += cost
        self.card.bonuses += cost * self.card.discount
        cost *= self.card.discount
        return cost

    def process_card(self):
        """
        Gold Card can not be upgraded.
        """
        pass
