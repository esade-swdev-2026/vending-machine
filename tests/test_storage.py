from pathlib import Path

import pytest

from vending_machine.models import MachineState, Product
from vending_machine.storage import read_coin_float, read_products, read_state, write_state


def test_read_products_and_coin_float(tmp_path: Path) -> None:
    products_file = tmp_path / "products.csv"
    products_file.write_text("slot,name,price_cents,quantity\n1,KitKat,130,5\n", encoding="utf-8")
    coins_file = tmp_path / "machine_coins_change.csv"
    coins_file.write_text("coin_cents,count\n50,3\n20,4\n", encoding="utf-8")
    assert read_products(products_file) == {1: Product(1, "KitKat", 130, 5)}
    assert read_coin_float(coins_file) == {50: 3, 20: 4}


def test_read_products_names_the_bad_line(tmp_path: Path) -> None:
    products_file = tmp_path / "products.csv"
    products_file.write_text(
        "slot,name,price_cents,quantity\n1,KitKat,130,5\n2,Water,cheap,3\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="line 3"):
        read_products(products_file)


def test_read_products_rejects_a_repeated_slot(tmp_path: Path) -> None:
    products_file = tmp_path / "products.csv"
    products_file.write_text(
        "slot,name,price_cents,quantity\n1,KitKat,130,5\n1,Water,100,3\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="slot 1 is repeated on line 3"):
        read_products(products_file)


def test_write_state_then_read_state_gives_the_same_machine(tmp_path: Path) -> None:
    state = MachineState({1: Product(1, "KitKat", 130, 4)}, {50: 3, 20: 0})
    products_file = tmp_path / "products.csv"
    coins_file = tmp_path / "machine_coins_change.csv"
    write_state(state, products_file, coins_file)
    assert read_state(products_file, coins_file) == state
    assert not list(tmp_path.glob("*.tmp"))
