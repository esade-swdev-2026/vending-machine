import pytest

from vending_machine.inventory import affordable_products, empty_slots, find_product, restock_slot
from vending_machine.models import Product, Products, UnknownSlot


def by_slot(*products: Product) -> Products:
    return {product.slot: product for product in products}


def test_return_possible_products_based_on_budget() -> None:
    products = by_slot(
        Product(1, "Choco bons", 200, 10),
        Product(2, "KitKat", 400, 5),
        Product(3, "Kinder Bueno", 350, 0),
    )
    result = affordable_products(products, credit_cents=300)
    assert result == [Product(1, "Choco bons", 200, 10)]


def test_return_no_products_if_out_of_stock() -> None:
    products = by_slot(
        Product(1, "Choco bons", 100, 0),
        Product(2, "KitKat", 200, 0),
    )
    result = affordable_products(products, credit_cents=500)
    assert result == []


def test_return_empty_list_if_budget_too_low() -> None:
    products = by_slot(
        Product(1, "Choco bons", 200, 10),
        Product(2, "KitKat", 400, 5),
    )
    result = affordable_products(products, credit_cents=100)
    assert result == []


def test_return_products_with_exact_budget() -> None:
    products = by_slot(
        Product(1, "Choco bons", 150, 10),
        Product(2, "KitKat", 150, 5),
    )
    result = affordable_products(products, credit_cents=150)
    assert result == list(products.values())


def test_return_empty_list_if_no_products_in_machine() -> None:
    products: Products = {}
    result = affordable_products(products, credit_cents=200)
    assert result == []


def test_find_product_returns_product_in_slot() -> None:
    products = by_slot(
        Product(1, "Choco bons", 150, 10),
        Product(2, "KitKat", 130, 5),
    )
    assert find_product(products, 2) == Product(2, "KitKat", 130, 5)


def test_find_product_raises_for_unknown_slot() -> None:
    with pytest.raises(UnknownSlot):
        find_product(by_slot(Product(1, "Choco bons", 150, 10)), 9)


def test_empty_slots_is_empty_when_every_slot_has_stock() -> None:
    products = by_slot(Product(1, "Choco bons", 150, 10), Product(2, "KitKat", 130, 5))
    assert empty_slots(products) == []


def test_empty_slots_lists_only_the_sold_out_products() -> None:
    products = by_slot(
        Product(1, "Choco bons", 150, 10),
        Product(2, "KitKat", 130, 0),
        Product(3, "Water", 100, 8),
    )
    assert empty_slots(products) == [Product(2, "KitKat", 130, 0)]


def test_empty_slots_lists_every_product_when_the_machine_is_empty() -> None:
    products = by_slot(Product(1, "Choco bons", 150, 0), Product(2, "KitKat", 130, 0))
    assert empty_slots(products) == list(products.values())


def test_restock_slot_fills_an_empty_slot() -> None:
    products = by_slot(Product(3, "Kinder Bueno", 180, 0))
    results = restock_slot(products, 3, 10)
    assert results[3] == Product(3, "Kinder Bueno", 180, 10)


def test_restock_slot_adds_to_the_units_already_there() -> None:
    products = by_slot(Product(2, "KitKat", 130, 5))
    results = restock_slot(products, 2, 3)
    assert results[2].quantity == 8


def test_restock_slot_leaves_the_original_products_unchanged() -> None:
    products = by_slot(Product(2, "KitKat", 130, 5))
    restock_slot(products, 2, 3)
    assert products[2].quantity == 5


def test_restock_slot_raises_for_unknown_slot() -> None:
    products = by_slot(Product(1, "Choco bons", 150, 10))
    with pytest.raises(UnknownSlot):
        restock_slot(products, 9, 5)


@pytest.mark.parametrize("units", [0, -3])
def test_restock_slot_rejects_zero_or_negative_units(units: int) -> None:
    with pytest.raises(ValueError, match="at least 1 unit"):
        restock_slot(by_slot(Product(2, "KitKat", 130, 5)), 2, units)
