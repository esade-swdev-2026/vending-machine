import pytest

from vending_machine.models import CannotMakeChange, InvalidCoin
from vending_machine.payment import credit_from_coins, make_change


def test_credit_is_the_sum_of_the_coins() -> None:
    assert credit_from_coins([100, 50, 20]) == 170


def test_credit_rejects_a_coin_that_is_not_accepted() -> None:
    with pytest.raises(InvalidCoin):
        credit_from_coins([100, 3])


def test_change_uses_largest_coins_first() -> None:
    assert make_change(70, {50: 5, 20: 5, 10: 5}) == [50, 20]


def test_change_never_uses_more_coins_than_the_machine_holds() -> None:
    assert make_change(100, {50: 1, 20: 2, 10: 5}) == [50, 20, 20, 10]


def test_no_change_for_exact_payment() -> None:
    assert make_change(0, {50: 5}) == []


def test_change_raises_when_amount_is_left_over() -> None:
    with pytest.raises(CannotMakeChange):
        make_change(30, {50: 5, 20: 1})
