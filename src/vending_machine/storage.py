import csv
from pathlib import Path

from vending_machine.models import Product


def read_products(path: Path) -> list[Product]:
    products = []
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                products.append(
                    Product(
                        slot=int(row["slot"]),
                        name=row["name"],
                        price_cents=int(row["price_cents"]),
                        quantity=int(row["quantity"]),
                    )
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad product on line {line_number}.") from error
    return products


def read_coin_float(path: Path) -> dict[int, int]:
    coin_float = {}
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                coin_float[int(row["coin_cents"])] = int(row["count"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad coin on line {line_number}.") from error
    return coin_float
