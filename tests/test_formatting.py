import pytest

from vending_machine.formatting import format_budget_message


def test_budget_formats_the_amount_correctly() -> None:
    currency = "€"
    amount = 2.55
    result = format_budget_message(currency, amount)
    assert result == "Your current balance is: 2.55€"


def test_budget_formats_different_currency() -> None:
    currency = "$"
    amount = 5.5
    result = format_budget_message(currency, amount)
    assert result == "Your current balance is: 5.50$"


def test_budget_rounds_correctly() -> None:
    currency = "€"
    amount = 2.558
    result = format_budget_message(currency, amount)
    assert result == "Your current balance is: 2.56€"


def test_budget_raises_value_error_for_negative_amount() -> None:
    with pytest.raises(ValueError):
        format_budget_message("€", -1.0)
