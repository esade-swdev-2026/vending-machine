from pathlib import Path

import pytest

from vending_machine.models import Product
from vending_machine.storage import read_coin_float, read_products


def test_read_products_and_coin_float(tmp_path: Path) -> None:
    products_file = tmp_path / "products.csv"
    products_file.write_text("slot,name,price_cents,quantity\n1,KitKat,130,5\n", encoding="utf-8")
    coins_file = tmp_path / "coins.csv"
    coins_file.write_text("coin_cents,count\n50,3\n20,4\n", encoding="utf-8")

    assert read_products(products_file) == [Product(1, "KitKat", 130, 5)]
    assert read_coin_float(coins_file) == {50: 3, 20: 4}


def test_read_products_names_the_bad_line(tmp_path: Path) -> None:
    products_file = tmp_path / "products.csv"
    products_file.write_text(
        "slot,name,price_cents,quantity\n1,KitKat,130,5\n2,Water,cheap,3\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="line 3"):
        read_products(products_file)
