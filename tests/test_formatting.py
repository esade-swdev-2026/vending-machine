from vending_machine.formatting import format_cents, format_change, format_product_lines
from vending_machine.models import Coins, Product


def test_format_cents_as_euros() -> None:
    amount_cents = 130
    assert format_cents(amount_cents) == "1.30 €"


def test_format_cents_below_one_euro() -> None:
    amount_cents = 5
    assert format_cents(amount_cents) == "0.05 €"


def test_format_product_lines_shows_sold_out() -> None:
    products = [Product(1, "KitKat", 130, 5), Product(2, "Kinder Bueno", 180, 0)]
    lines = format_product_lines(products)
    assert "KitKat" in lines[0] and "1.30 €" in lines[0]
    assert "SOLD OUT" in lines[1]


def test_format_change_lists_each_coin_with_its_count() -> None:
    change = {20: 2, 50: 1}
    assert format_change(change) == "1 x 0.50 € + 2 x 0.20 €"


def test_format_change_for_exact_payment() -> None:
    change: Coins = {}
    assert format_change(change) == "none"
