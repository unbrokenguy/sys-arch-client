from dataclasses import dataclass
from typing import List

from cafe.menu import MenuEntry
from cafe.customer import Customer
from cafe.menu import MozzarellaPizza, Borscht, Tea


@dataclass
class Order:
    """Class that represents Order in Cafe.

    DataClass with __init__, __eq__ and __repr__ methods that built in.

    Attributes:
        customer: A Customer from cafe.Customer.
        order: A list that contains all menu entries that orders a customer.
    """
    customer: Customer
    order: List[MenuEntry]

    def __dict__(self) -> dict:
        """Return Order object in dict format.

        Returns:
            dict: A dictionary with all data about customer and order.
        """
        order_dict = {}
        order_dict.update({"customer": self.customer.__dict__()})
        order_dict.update({"order": [vars(o) for o in self.order]})
        return order_dict

    def add_entry(self, entry: MenuEntry):
        """Add MenuEntry to order list"""
        self.order.append(entry)

    def remove_entry(self, entry: MenuEntry):
        """Remove MenuEntry from order list"""
        self.order.remove(entry)


class OrderFactory:
    """Order factory.
    Factory makes orders from list of dishes names or can make single MenuEntry by its name
    """

    def create_entry(self, entry_name):
        """Make single MenuEntry by its name.
        Args:
            entry_name: A string with name of dish.
        Raises:
            ValueError: An error occurred if dish name isn't in menu.
        """
        if entry_name == "MozzarellaPizza":
            return MozzarellaPizza()
        elif entry_name == "Borscht":
            return Borscht()
        elif entry_name == "Tea":
            return Tea()
        else:
            raise ValueError

    def create_order(self, customer, order) -> Order:
        """Create new Order object.
        Args:
            customer: A Customer who makes order.
            order: A list of strings with names of dishes.
        Returns:
            Order object with customer and order.
        """
        o = Order(customer=customer, order=[])
        for entry in order:
            o.add_entry(self.create_entry(entry))
        return o
