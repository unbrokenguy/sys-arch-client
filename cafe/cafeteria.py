import os
import smtplib
import ssl
from dataclasses import dataclass

from cafe.customer import SilverCardStrategy, GoldCardStrategy
from cafe.order import OrderFactory, Order


@dataclass
class Receipt:
    order: Order

    def make(self):
        total_cost = sum(map(lambda o: o['cost'], self.order.__dict__()['order']))
        discount_strategy = None
        if self.order.customer.card.level == "silver":
            discount_strategy = SilverCardStrategy(self.order.customer.card)
        if self.order.customer.card.level == "gold":
            discount_strategy = GoldCardStrategy(self.order.customer.card)
        total_cost -= discount_strategy.make_discount(total_cost)
        result = self.order.__dict__()
        result.update({"total cost": total_cost})
        return result


class ReceiptEmail:
    def __init__(self, order: Order):
        self.receipt = Receipt(order)

        self.credentials = {"login": os.getenv("test_mail"), "password": os.getenv("test_mail_passwd")}

    def send_to_email(self, *args, **kwargs):
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(self.credentials["login"], self.credentials["password"])
            server.sendmail(self.credentials["login"], kwargs["email"], str(self.receipt.make()))
        return self.receipt.make()

    def make(self):
        return self.receipt.make()


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Cafe(metaclass=SingletonMeta):
    customers = []
    orders = {}
    order_factory = OrderFactory()

    def receipt(self, customer, *args):
        if args[0] == "email":
            ReceiptEmail(
                order=self.orders[customer.name],
            ).send_to_email(email=customer.email)
            self.customers.remove(customer)
            self.orders.pop(customer.name, None)
            return True
        elif args[0] == "receipt":
            receipt = Receipt(order=self.orders[customer.name]).make()
            self.customers.remove(customer)
            self.orders.pop(customer.name, None)
            return receipt
        else:
            raise NotImplementedError

    def make_order(self, customer, *args):
        if customer not in self.customers:
            self.customers.append(customer)
            self.orders[customer.name] = self.order_factory.create_order(customer, args)
        else:
            raise ValueError("You can only edit your order.")

    def edit_order(self, customer, *args):
        if customer.name in self.orders.keys():
            if args[0] == "add":
                self.orders[customer.name].add_entry(self.order_factory.create_entry(entry_name=args[1]))
            elif args[0] == "remove":
                self.orders[customer.name].remove_entry(self.order_factory.create_entry(entry_name=args[1]))
            else:
                raise ValueError("You can't do that.")
        else:
            raise ValueError("You can only create new order.")