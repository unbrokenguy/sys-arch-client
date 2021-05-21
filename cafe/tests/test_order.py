import pytest
from cafe.customer import Customer, Card
from cafe.menu import Tea, Borscht, MozzarellaPizza
from cafe.order import Order, OrderFactory


@pytest.mark.order
def test_order_remove_entry_fail():
    """
    Unit Test
    """
    customer = Customer(name="Micky", card=Card())
    order = Order(customer=customer, order=[Tea(), Borscht()])
    with pytest.raises(ValueError):
        order.remove_entry(MozzarellaPizza())


@pytest.mark.order
def test_order_factory_create_entry_fail():
    """
    Unit Test
    """
    factory = OrderFactory()
    with pytest.raises(ValueError):
        factory.create_entry("IceCream")


@pytest.mark.order
def test_order_factory_create_order_fail():
    """
    Unit Test
    """
    factory = OrderFactory()
    customer = Customer(name="Micky", card=Card())
    with pytest.raises(ValueError):
        factory.create_order(customer=customer, order=["Tea", "Borscht", "IceCream"])