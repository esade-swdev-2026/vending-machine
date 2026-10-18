import pytest

from vending_machine.models import CannotMakeChange, InvalidCoin
from vending_machine.payment import add_coins, credit_from_coins, make_change


def test_credit_is_the_value_of_every_coin_times_its_count() -> None:
    assert credit_from_coins({100: 1, 50: 2, 20: 1}) == 220


def test_credit_rejects_a_coin_that_is_not_accepted() -> None:
    with pytest.raises(InvalidCoin):
        credit_from_coins({100: 1, 3: 1})


def test_credit_rejects_a_negative_count() -> None:
    with pytest.raises(InvalidCoin):
        credit_from_coins({100: -1})


def test_change_uses_largest_coins_first() -> None:
    assert make_change(70, {50: 5, 20: 5, 10: 5}) == {50: 1, 20: 1}


def test_change_never_uses_more_coins_than_the_machine_holds() -> None:
    assert make_change(100, {50: 1, 20: 2, 10: 5}) == {50: 1, 20: 2, 10: 1}


def test_no_change_for_exact_payment() -> None:
    assert make_change(0, {50: 5}) == {}


def test_change_raises_when_amount_is_left_over() -> None:
    with pytest.raises(CannotMakeChange):
        make_change(30, {50: 5, 20: 1})


def test_change_backs_off_a_big_coin_when_the_rest_cannot_be_paid() -> None:
    assert make_change(60, {50: 1, 20: 3}) == {20: 3}


def test_add_coins_counts_both_handfuls() -> None:
    assert add_coins({50: 1, 20: 2}, {20: 1, 100: 1}) == {50: 1, 20: 3, 100: 1}
