from vending_machine.inventory import get_possible_products_by_budget
from vending_machine.models import ProductDetails


def test_return_possible_products_based_on_budget() -> None:
    products_in_machine = {
        "Choco bons": ProductDetails(10, 2.0),
        "KitKat": ProductDetails(5, 4.0),
        "Kinder Bueno": ProductDetails(0, 2.0),
    }
    result = get_possible_products_by_budget(products_in_machine, budget=3.0)
    assert result == ["Choco bons"]


def test_return_no_products_if_out_of_stock() -> None:
    products_in_machine = {
        "Choco bons": ProductDetails(0, 1.0),
        "KitKat": ProductDetails(0, 2.0),
    }
    result = get_possible_products_by_budget(products_in_machine, budget=5.0)
    assert result == []


def test_return_empty_list_if_budget_too_low() -> None:
    products_in_machine = {
        "Choco bons": ProductDetails(10, 2.0),
        "KitKat": ProductDetails(5, 4.0),
    }
    result = get_possible_products_by_budget(products_in_machine, budget=1.0)
    assert result == []


def test_return_products_with_exact_budget() -> None:
    products_in_machine = {
        "Choco bons": ProductDetails(5, 1.5),
        "KitKat": ProductDetails(10, 1.5),
    }
    result = get_possible_products_by_budget(products_in_machine, budget=1.5)
    assert result == ["Choco bons", "KitKat"]


def test_return_empty_list_if_no_products_in_machine() -> None:
    products_in_machine: dict[str, ProductDetails] = {}
    result = get_possible_products_by_budget(products_in_machine, budget=2.0)
    assert result == []
