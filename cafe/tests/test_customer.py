import pytest

from cafe.cafeteria import Cafe
from cafe.customer import Customer, Card, SilverCardStrategy, GoldCardStrategy


@pytest.mark.customer
def test_receipt_with_gold_card_success():
    """
    Functional Test
    """
    cafe = Cafe()
    customer = Customer(name="Turkish", card=Card(level="gold", discount=0.1, total_spent=10001))
    cafe.make_order(customer, "MozzarellaPizza")
    receipt_gold = cafe.receipt(customer, "receipt")
    customer_silver = Customer(name="Pulford", card=Card())
    cafe.make_order(customer_silver, "MozzarellaPizza")
    receipt_silver = cafe.receipt(customer_silver, "receipt")
    assert customer.card.level == "gold"
    assert customer_silver.card.level == "silver"
    assert receipt_silver["total cost"] > receipt_gold["total cost"]


@pytest.mark.customer
def test_silver_card_upgrade_success():
    """
    Unit Test
    """
    card = Card()
    strategy = SilverCardStrategy(card=card)
    strategy.make_discount(cost=10001)
    assert card.level == "gold"
    assert card.total_spent == 10001


@pytest.mark.customer
def test_gold_card_process_success():
    """
    Unit Test
    """
    card = Card(level="gold")
    strategy = GoldCardStrategy(card=card)
    nothing = strategy.process_card()
    assert nothing is None

