import pytest
from cafe.cafe import Cafe, Receipt, ReceiptEmail
from cafe.customer import Customer


@pytest.mark.cafe
def test_cafe_make_order_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    cafe.make_order(customer, "Tea", "Borscht", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3


@pytest.mark.cafe
def test_cafe_make_order_fail():
    cafe = Cafe()
    customer = Customer(name="Micky")
    with pytest.raises(ValueError):
        cafe.make_order(customer, "Tea", "Borscht", "Tea")


@pytest.mark.cafe
def test_cafe_edit_order_fail():
    cafe = Cafe()
    customer = Customer(name="Boris")
    with pytest.raises(ValueError):
        cafe.edit_order(customer, "Tea", "Borscht", "Tea")


@pytest.mark.cafe
def test_cafe_edit_order_remove_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    cafe.edit_order(customer, "remove", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 2


@pytest.mark.cafe
def test_cafe_edit_order_add_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    cafe.edit_order(customer, "add", "MozzarellaPizza")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3
    assert cafe.orders[customer.name].order[2].__class__.__name__ == "MozzarellaPizza"


@pytest.mark.cafe
def test_cafe_edit_order_unknown_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    with pytest.raises(ValueError):
        cafe.edit_order(customer, "check", "MozzarellaPizza")


@pytest.mark.cafe
def test_cafe_customers_success():
    cafe = Cafe()
    assert len(cafe.customers) == 1
    assert cafe.customers[0].name == "Micky"


@pytest.mark.cafe
def test_cafe_receipt_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    order = {}
    order.update(vars(customer))
    order.update(cafe.orders[customer.name].__dict__())
    receipt = cafe.receipt(customer, "receipt")
    assert len(cafe.customers) == 0
    assert customer.name not in cafe.orders.keys()
    assert receipt == order


@pytest.mark.cafe
def test_cafe_receipt_receipt_unknown_success():
    cafe = Cafe()
    customer = Customer(name="Micky")
    with pytest.raises(NotImplementedError):
        cafe.receipt(customer, "unknown")


@pytest.mark.cafe
def test_cafe_receipt_email_success():
    cafe = Cafe()
    customer = Customer(name="Tommy", email="khazievbulatphanzilovich@gmail.com")
    cafe.make_order(customer, "Tea", "Borscht", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3
    cafe.receipt(customer, "email")
    assert len(cafe.customers) == 0
    assert customer.name not in cafe.orders.keys()


@pytest.mark.cafe
def test_receipt_and_email_success():
    cafe = Cafe()
    customer = Customer(name="Vinny", email="khazievbulatphanzilovich@gmail.com")
    cafe.make_order(customer, "MozzarellaPizza")
    order = {}
    order.update(vars(customer))
    order.update(cafe.orders[customer.name].__dict__())
    receipt = Receipt(cafe.orders[customer.name])
    receipt_email = ReceiptEmail(cafe.orders[customer.name])
    receipt = receipt.make()
    receipt_email = receipt_email.make()
    assert receipt == order
    assert receipt == receipt_email
