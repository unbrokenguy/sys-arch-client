from copy import copy

import pytest
from cafe.cafeteria import Cafe, Receipt, ReceiptEmail
from cafe.customer import Customer, Card, SilverCardStrategy


@pytest.fixture
def cafe():
    return Cafe()


customer_micky = Customer(name="Micky", card=Card())


@pytest.fixture
def micky():
    return customer_micky


#  Micky test chain. 1 test.
@pytest.mark.cafe
def test_cafe_make_order_success(cafe, micky):
    """
    Unit Test
    """
    cafe.make_order(micky, "Tea", "Borscht", "Tea")
    assert micky in cafe.customers
    assert micky.name in cafe.orders.keys()
    assert len(cafe.orders[micky.name].order) == 3


#  Micky test chain. 2 test.
@pytest.mark.cafe
def test_cafe_make_order_fail(cafe, micky):
    """
    Unit Test
    """
    with pytest.raises(ValueError):
        cafe.make_order(micky, "Tea", "Borscht", "Tea")


#  Micky test chain. 3 test.
@pytest.mark.cafe
def test_cafe_edit_order_remove_success(cafe, micky):
    """
    Unit Test
    """
    cafe.edit_order(micky, "remove", "Tea")
    assert micky in cafe.customers
    assert micky.name in cafe.orders.keys()
    assert len(cafe.orders[micky.name].order) == 2


#  Micky test chain. 4 test.
@pytest.mark.cafe
def test_cafe_edit_order_add_success(cafe, micky):
    """
    Unit Test
    """
    cafe.edit_order(micky, "add", "MozzarellaPizza")
    assert micky in cafe.customers
    assert micky.name in cafe.orders.keys()
    assert len(cafe.orders[micky.name].order) == 3
    assert cafe.orders[micky.name].order[2].__class__.__name__ == "MozzarellaPizza"


#  Micky test chain. 5 test.
@pytest.mark.cafe
def test_cafe_unknown_edit_order_fail(cafe, micky):
    """
    Unit Test
    """
    with pytest.raises(ValueError):
        cafe.edit_order(micky, "double", "Tea")


#  Micky test chain. 6 test.
@pytest.mark.cafe
def test_cafe_receipt_success(cafe, micky):
    """
    Unit Test
    """
    receipt = cafe.receipt(micky, "receipt")
    assert len(cafe.customers) == 0
    assert micky.name not in cafe.orders.keys()
    assert "total cost" in receipt.keys()


#  Micky test chain. 7 test.
@pytest.mark.cafe
def test_cafe_receipt_receipt_unknown_success(cafe, micky):
    """
    Unit Test
    """
    with pytest.raises(NotImplementedError):
        cafe.receipt(micky, "unknown")


#  Micky test chain. 8 test.
@pytest.mark.cafe
def test_cafe_edit_order_unknown_success(cafe, micky):
    """
    Unit Test
    """
    with pytest.raises(ValueError):
        cafe.edit_order(micky, "check", "MozzarellaPizza")


@pytest.mark.cafe
def test_cafe_known_edit_order_fail(cafe):
    """
    Unit Test
    """
    customer = Customer(name="Boris", card=Card())
    with pytest.raises(ValueError):
        cafe.edit_order(customer, "add", "Tea")


@pytest.mark.cafe
def test_cafe_receipt_email_success(cafe):
    """
    Unit Test
    """
    customer = Customer(name="Tommy", email="khazievbulatphanzilovich@gmail.com", card=Card())
    cafe.make_order(customer, "Tea", "Borscht", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3
    cafe.receipt(customer, "email")
    assert len(cafe.customers) == 0
    assert customer.name not in cafe.orders.keys()


@pytest.mark.cafe
def test_receipt_and_email_success(cafe):
    """
    Unit Test
    """
    customer = Customer(name="Vinny", email="khazievbulatphanzilovich@gmail.com", card=Card())
    cafe.make_order(customer, "MozzarellaPizza")
    receipt = Receipt(cafe.orders[customer.name])
    receipt_email = ReceiptEmail(cafe.orders[customer.name])
    receipt = receipt.make()
    receipt_email = receipt_email.make()
    assert "total cost" in receipt.keys()
    assert "total cost" in receipt_email.keys()
    assert receipt == receipt_email
