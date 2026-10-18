import pytest

from vending_machine.inventory import affordable_products, find_product
from vending_machine.models import Product, UnknownSlot


def test_return_possible_products_based_on_budget() -> None:
    products = [
        Product(1, "Choco bons", 200, 10),
        Product(2, "KitKat", 400, 5),
        Product(3, "Kinder Bueno", 350, 0),
    ]
    result = affordable_products(products, credit_cents=300)
    assert result == [Product(1, "Choco bons", 200, 10)]


def test_return_no_products_if_out_of_stock() -> None:
    products = [
        Product(1, "Choco bons", 100, 0),
        Product(2, "KitKat", 200, 0),
    ]
    result = affordable_products(products, credit_cents=500)
    assert result == []


def test_return_empty_list_if_budget_too_low() -> None:
    products = [
        Product(1, "Choco bons", 200, 10),
        Product(2, "KitKat", 400, 5),
    ]
    result = affordable_products(products, credit_cents=100)
    assert result == []


def test_return_products_with_exact_budget() -> None:
    products = [
        Product(1, "Choco bons", 150, 10),
        Product(2, "KitKat", 150, 5),
    ]
    result = affordable_products(products, credit_cents=150)
    assert result == products


def test_return_empty_list_if_no_products_in_machine() -> None:
    products: list[Product] = []
    result = affordable_products(products, credit_cents=200)
    assert result == []


def test_find_product_returns_product_in_slot() -> None:
    products = [Product(1, "Choco bons", 150, 10), Product(2, "KitKat", 130, 5)]
    assert find_product(products, 2) == Product(2, "KitKat", 130, 5)


def test_find_product_raises_for_unknown_slot() -> None:
    with pytest.raises(UnknownSlot):
        find_product([Product(1, "Choco bons", 150, 10)], 9)
