import pytest
from cafe.customer import Customer
from cafe.menu import Tea, Borscht, MozzarellaPizza
from cafe.order import Order, OrderFactory


@pytest.mark.order
def test_order_remove_entry_fail():
    customer = Customer(name="Micky")
    order = Order(customer=customer, order=[Tea(), Borscht()])
    with pytest.raises(ValueError):
        order.remove_entry(MozzarellaPizza())


@pytest.mark.order
def test_order_factory_create_entry_fail():
    factory = OrderFactory()
    with pytest.raises(ValueError):
        factory.create_entry("IceCream")


@pytest.mark.order
def test_order_factory_create_order_fail():
    factory = OrderFactory()
    customer = Customer(name="Micky")
    with pytest.raises(ValueError):
        factory.create_order(customer=customer, order=["Tea", "Borscht", "IceCream"])
