import pytest
from typer.testing import CliRunner

from vending_machine.cli import (
    Products_details,
    app,
    display_possible_products_by_budget,
    format_budget_message,
)

runner = CliRunner()


def test_cli_rejects_non_positive_amount_with_exit_code() -> None:
    result = runner.invoke(app, ["display-budget", "€", "--amount", "-1"])
    assert result.exit_code == 1
    assert "Invalid amount." in result.stdout


def test_budget_formats_the_amount_correctly() -> None:
    result = format_budget_message("€", 2.55)
    assert result == "Your current balance is: 2.55€"


def test_budget_formats_different_currency() -> None:
    result = format_budget_message("$", 5.5)
    assert result == "Your current balance is: 5.50$"


def test_budget_rounds_correctly() -> None:
    result = format_budget_message("€", 2.558)
    assert result == "Your current balance is: 2.56€"


def test_budget_raises_value_error_for_negative_amount() -> None:
    with pytest.raises(ValueError):
        format_budget_message("€", -1.0)


def test_return_possible_products_based_on_budget() -> None:
    products_in_machine = {
        "Choco bons": Products_details(10, 2.0),
        "KitKat": Products_details(5, 4.0),
        "Kinder Bueno": Products_details(0, 2.0),
    }
    result = display_possible_products_by_budget(products_in_machine, budget=3.0)
    assert result == ["Choco bons"]


def test_return_no_products_if_out_of_stock() -> None:
    products_in_machine = {
        "Choco bons": Products_details(0, 1.0),
        "KitKat": Products_details(0, 2.0),
    }
    result = display_possible_products_by_budget(products_in_machine, budget=5.0)
    assert result == []


def test_return_empty_list_if_budget_too_low() -> None:
    products_in_machine = {
        "Choco bons": Products_details(10, 2.0),
        "KitKat": Products_details(5, 4.0),
    }
    result = display_possible_products_by_budget(products_in_machine, budget=1.0)
    assert result == []


def test_return_products_with_exact_budget() -> None:
    products_in_machine = {
        "Choco bons": Products_details(5, 1.5),
        "KitKat": Products_details(10, 1.5),
    }
    result = display_possible_products_by_budget(products_in_machine, budget=1.5)
    assert result == ["Choco bons", "KitKat"]


def test_return_empty_list_if_no_products_in_machine() -> None:
    products_in_machine: dict[str, Products_details] = {}
    result = display_possible_products_by_budget(products_in_machine, budget=2.0)
    assert result == []
