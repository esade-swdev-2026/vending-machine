import pytest

from vending_machine.machine import sell
from vending_machine.models import (
    InsufficientCredit,
    InvalidCoin,
    Product,
    Sale,
    SoldOut,
    UnknownSlot,
)

PRODUCTS = [Product(1, "KitKat", 130, 5), Product(2, "Kinder Bueno", 180, 0)]
COIN_FLOAT = {50: 5, 20: 5, 10: 5}


def test_sell_returns_the_product_and_the_change() -> None:
    assert sell(PRODUCTS, 1, [200], COIN_FLOAT) == Sale(PRODUCTS[0], [50, 20])


def test_sell_does_not_change_its_inputs() -> None:
    products = list(PRODUCTS)
    coin_float = dict(COIN_FLOAT)
    sell(products, 1, [200], coin_float)
    assert products == PRODUCTS
    assert coin_float == COIN_FLOAT


def test_sell_raises_for_unknown_slot() -> None:
    with pytest.raises(UnknownSlot):
        sell(PRODUCTS, 9, [200], COIN_FLOAT)


def test_sell_raises_when_sold_out() -> None:
    with pytest.raises(SoldOut):
        sell(PRODUCTS, 2, [200], COIN_FLOAT)


def test_sell_raises_for_invalid_coin() -> None:
    with pytest.raises(InvalidCoin):
        sell(PRODUCTS, 1, [3], COIN_FLOAT)


def test_sell_raises_when_credit_is_too_low() -> None:
    with pytest.raises(InsufficientCredit):
        sell(PRODUCTS, 1, [100], COIN_FLOAT)
