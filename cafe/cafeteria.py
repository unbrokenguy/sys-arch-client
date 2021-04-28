import os
import smtplib
import ssl
from dataclasses import dataclass

from cafe.customer import SilverCardStrategy, GoldCardStrategy
from cafe.order import OrderFactory, Order


@dataclass
class Receipt:
    """Receipt class.
    Methods:
        make: Calculate total cost of the order, makes a discount by card level.
    DataClass with __init__, __eq__ and __repr__ methods that built in.

    Attributes:
        order: The order for which we want to receive a check.
    """
    order: Order

    def make(self):
        """
        Calculate total cost of the order, makes a discount by card level.
        Returns:
            A dictionary with information about order and total cost.
        """
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
    """Receipt Class decorator, so receipt can be send by email.
    Attributes:
        receipt: Receipt object.
        credentials: Credentials of email service.
    Methods:
        make: Calculate total cost of the order, makes a discount by card level.
        send_to_email: Send result of make function by email.
    """
    def __init__(self, order: Order):
        """Initializes receipt with order and credentials"""
        self.receipt = Receipt(order)

        self.credentials = {"login": os.getenv("test_mail"), "password": os.getenv("test_mail_passwd")}

    def send_to_email(self):
        """Wraps receipt.make() function.
        And send email to a customer.
        Returns:
            A dictionary with information about order and total cost.
        """
        context = ssl.create_default_context()
        result = self.receipt.make()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(self.credentials["login"], self.credentials["password"])
            server.sendmail(self.credentials["login"], self.receipt.order.customer.email, str(result))
        return result

    def make(self):
        """Change behaviour of Receipt make function. So it can send email.
        Returns:
            A dictionary with information about order and total cost.
        """
        return self.send_to_email()


class SingletonMeta(type):
    """
    Metaclass realization of SingleTon.
    Attributes:
        _instances: A dict where class name is key and instance is value.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        When class was called "class()", checking if instance of class exists returns it,
        else class instance created with *args and **kwargs.
        Args:
            *args: positional arguments.
            **kwargs: keyword arguments.

        Returns:
            Called class instance
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Cafe(metaclass=SingletonMeta):
    """
    Singleton
    Cafe is a class that contain customers and their orders.
    Cafe make order from Customer list of dishes, add or remove dish from customers order.
    Attributes:
        customers: List of Customers.
        orders: Dictionary Customer name is the key and Order object is the value.
        order_Factory: Order Factory.
    """
    customers = []
    orders = {}
    order_factory = OrderFactory()

    def receipt(self, customer, method):
        """Makes Receipt.
        If method value is "email", send receipt to customers email.

        Args:
            customer: Customer who wants receipt.
            method: String how to customer wants to get receipt.
        Returns:
            Receipt regardless of method.
        Raises:
            NotImplementedError: If method not "email" or "receipt".
        """
        if method == "email":
            receipt = ReceiptEmail(
                order=self.orders[customer.name],
            ).make()
        elif method == "receipt":
            receipt = Receipt(order=self.orders[customer.name]).make()
        else:
            raise NotImplementedError
        self.customers.remove(customer)
        self.orders.pop(customer.name, None)
        return receipt

    def make_order(self, customer, *args):
        """
        Makes order with a list of dishes names.
        Args:
            customer: Customer who wants to make an order.
            *args: List of dishes names.
        Raises:
            ValueError if customer already has order.
        """
        if customer not in self.customers:
            self.customers.append(customer)
            self.orders[customer.name] = self.order_factory.create_order(customer, args)
        else:
            raise ValueError("You can only edit your order.")

    def edit_order(self, customer, method, entry):
        """
        Add or remove dish from the customers order.
        Args:
            customer: Customer who wants to make an order.
            method: String with method, "add" or "remove".
            entry: String with dish name.
         Raises:
            ValueError if customer has order or wrong method.
        """
        if customer.name in self.orders.keys():
            if method == "add":
                self.orders[customer.name].add_entry(self.order_factory.create_entry(entry_name=entry))
            elif method == "remove":
                self.orders[customer.name].remove_entry(self.order_factory.create_entry(entry_name=entry))
            else:
                raise ValueError("You can't do that.")
        else:
            raise ValueError("You can only create new order.")
