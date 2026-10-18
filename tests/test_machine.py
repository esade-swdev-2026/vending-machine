import pytest

from vending_machine.machine import sell
from vending_machine.models import (
    CannotMakeChange,
    Coins,
    InsufficientCredit,
    InvalidCoin,
    MachineState,
    Product,
    Sale,
    SoldOut,
    UnknownSlot,
)

KITKAT = Product(1, "KitKat", 130, 5)
PRODUCTS = {1: KITKAT, 2: Product(2, "Kinder Bueno", 180, 0)}
STATE = MachineState(PRODUCTS, {50: 5, 20: 5, 10: 5})


def total_cents(coins: Coins) -> int:
    return sum(coin * count for coin, count in coins.items())


def test_sell_returns_the_product_and_the_change() -> None:
    assert sell(STATE, 1, {200: 1}).sale == Sale(KITKAT, {50: 1, 20: 1})


def test_sell_takes_one_unit_out_of_stock() -> None:
    assert sell(STATE, 1, {200: 1}).state.products[1].quantity == 4


def test_sell_keeps_the_inserted_coins_and_removes_the_change() -> None:
    new_float = sell(STATE, 1, {200: 1}).state.coin_float
    assert new_float == {200: 1, 50: 4, 20: 4, 10: 5}


def test_money_in_the_machine_grows_by_the_price() -> None:
    new_float = sell(STATE, 1, {100: 1, 50: 1}).state.coin_float
    assert total_cents(new_float) == total_cents(STATE.coin_float) + KITKAT.price_cents


def test_selling_the_last_unit_sells_the_product_out() -> None:
    state = MachineState({1: Product(1, "KitKat", 130, 1)}, {})
    after = sell(state, 1, {100: 1, 20: 1, 10: 1}).state
    with pytest.raises(SoldOut):
        sell(after, 1, {100: 1, 20: 1, 10: 1})


def test_sell_does_not_change_the_state_it_was_given() -> None:
    state = MachineState(dict(PRODUCTS), {50: 5, 20: 5, 10: 5})
    sell(state, 1, {200: 1})
    assert state == STATE


def test_sell_can_give_back_coins_the_customer_just_inserted() -> None:
    state = MachineState(PRODUCTS, {50: 0, 20: 0})
    assert sell(state, 1, {100: 1, 20: 2, 10: 1}).sale == Sale(KITKAT, {20: 1})


def test_sell_raises_for_unknown_slot() -> None:
    with pytest.raises(UnknownSlot):
        sell(STATE, 9, {200: 1})


def test_sell_raises_when_sold_out() -> None:
    with pytest.raises(SoldOut):
        sell(STATE, 2, {200: 1})


def test_sell_raises_for_invalid_coin() -> None:
    with pytest.raises(InvalidCoin):
        sell(STATE, 1, {3: 1})


def test_sell_raises_when_credit_is_too_low() -> None:
    with pytest.raises(InsufficientCredit):
        sell(STATE, 1, {100: 1})


def test_sell_raises_when_change_cannot_be_made() -> None:
    with pytest.raises(CannotMakeChange):
        sell(MachineState(PRODUCTS, {}), 1, {200: 1})
