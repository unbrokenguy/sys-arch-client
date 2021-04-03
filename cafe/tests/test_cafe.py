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


@pytest.mark.cafe
def test_cafe_make_order_success(cafe, micky):
    customer = micky
    cafe.make_order(customer, "Tea", "Borscht", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3


@pytest.mark.cafe
def test_cafe_make_order_fail(cafe, micky):
    customer = micky
    with pytest.raises(ValueError):
        cafe.make_order(customer, "Tea", "Borscht", "Tea")


@pytest.mark.cafe
def test_cafe_edit_order_fail(cafe):
    cafe = Cafe()
    customer = Customer(name="Boris", card=Card())
    with pytest.raises(ValueError):
        cafe.edit_order(customer, "Tea", "Borscht", "Tea")


@pytest.mark.cafe
def test_cafe_edit_order_remove_success():
    cafe = Cafe()
    customer = Customer(name="Micky", card=Card())
    cafe.edit_order(customer, "remove", "Tea")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 2


@pytest.mark.cafe
def test_cafe_edit_order_add_success(cafe, micky):
    customer = micky
    cafe.edit_order(customer, "add", "MozzarellaPizza")
    assert customer in cafe.customers
    assert customer.name in cafe.orders.keys()
    assert len(cafe.orders[customer.name].order) == 3
    assert cafe.orders[customer.name].order[2].__class__.__name__ == "MozzarellaPizza"


@pytest.mark.cafe
def test_cafe_edit_order_unknown_success(cafe, micky):
    customer = micky
    with pytest.raises(ValueError):
        cafe.edit_order(customer, "check", "MozzarellaPizza")


@pytest.mark.cafe
def test_cafe_customers_success(cafe):
    assert len(cafe.customers) == 1
    assert cafe.customers[0].name == "Micky"


@pytest.mark.cafe
def test_cafe_receipt_success(cafe, micky):
    customer = micky
    receipt = cafe.receipt(customer, "receipt")
    assert len(cafe.customers) == 0
    assert customer.name not in cafe.orders.keys()
    assert "total cost" in receipt.keys()


@pytest.mark.cafe
def test_cafe_receipt_receipt_unknown_success(cafe, micky):
    customer = micky
    with pytest.raises(NotImplementedError):
        cafe.receipt(customer, "unknown")


@pytest.mark.cafe
def test_cafe_receipt_email_success(cafe):
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
    customer = Customer(name="Vinny", email="khazievbulatphanzilovich@gmail.com", card=Card())
    cafe.make_order(customer, "MozzarellaPizza")
    receipt = Receipt(cafe.orders[customer.name])
    receipt_email = ReceiptEmail(cafe.orders[customer.name])
    receipt = receipt.make()
    receipt_email = receipt_email.make()
    assert "total cost" in receipt.keys()
    assert "total cost" in receipt_email.keys()
    assert receipt == receipt_email


@pytest.mark.cafe
def test_receipt_with_gold_card_success(cafe):
    card = Card()
    strategy = SilverCardStrategy(card=card)
    strategy.make_discount(cost=10001)
    vinny = Customer(name="Vinny", card=card)
    boris = Customer(name="Boris", card=Card())
    cafe.make_order(vinny, "MozzarellaPizza")
    cafe.make_order(boris, "MozzarellaPizza")
    receipt_vinny = Receipt(cafe.orders[vinny.name]).make()
    receipt_boris = Receipt(cafe.orders[boris.name]).make()
    assert card.level == "gold"
    assert receipt_vinny["total cost"] < receipt_boris["total cost"]
