from vending_machine.formatting import format_cents, format_product_lines
from vending_machine.models import Product


def test_format_cents_as_euros() -> None:
    assert format_cents(130) == "1.30 €"


def test_format_cents_below_one_euro() -> None:
    assert format_cents(5) == "0.05 €"


def test_format_product_lines_shows_sold_out() -> None:
    products = [Product(1, "KitKat", 130, 5), Product(2, "Kinder Bueno", 180, 0)]
    lines = format_product_lines(products)
    assert "KitKat" in lines[0] and "1.30 €" in lines[0]
    assert "SOLD OUT" in lines[1]
