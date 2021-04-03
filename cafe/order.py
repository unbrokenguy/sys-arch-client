from dataclasses import dataclass

from cafe.menu import MenuEntry
from cafe.customer import Customer
from cafe.menu import MozzarellaPizza, Borscht, Tea


@dataclass
class Order:
    customer: Customer
    order: []

    def __dict__(self) -> dict:
        order_dict = {}
        order_dict.update({"customer": self.customer.__dict__()})
        order_dict.update({"order": []})
        for o in self.order:
            order_dict["order"].append(vars(o))
        return order_dict

    def add_entry(self, entry: MenuEntry):
        self.order.append(entry)

    def remove_entry(self, entry: MenuEntry):
        self.order.remove(entry)


class OrderFactory:
    def create_entry(self, entry_name):
        if entry_name == "MozzarellaPizza":
            return MozzarellaPizza()
        elif entry_name == "Borscht":
            return Borscht()
        elif entry_name == "Tea":
            return Tea()
        else:
            raise ValueError

    def create_order(self, customer, order) -> Order:
        o = Order(customer=customer, order=[])
        for entry in order:
            o.add_entry(self.create_entry(entry))
        return o
