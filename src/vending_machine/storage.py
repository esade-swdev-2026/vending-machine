import csv
from pathlib import Path

from vending_machine.models import Coins, MachineState, Product, Products

PRODUCT_COLUMNS = ["slot", "name", "price_cents", "quantity"]
COIN_COLUMNS = ["coin_cents", "count"]


def read_products(path: Path) -> Products:
    products: Products = {}
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                product = Product(
                    slot=int(row["slot"]),
                    name=row["name"],
                    price_cents=int(row["price_cents"]),
                    quantity=int(row["quantity"]),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad product on line {line_number}.") from error
            if product.slot in products:
                raise ValueError(f"{path}: slot {product.slot} is repeated on line {line_number}.")
            products[product.slot] = product
    return products


def read_coin_float(path: Path) -> Coins:
    coin_float = {}
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                coin_float[int(row["coin_cents"])] = int(row["count"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad coin on line {line_number}.") from error
    return coin_float


def read_state(products_path: Path, coins_path: Path) -> MachineState:
    return MachineState(read_products(products_path), read_coin_float(coins_path))


def write_state(state: MachineState, products_path: Path, coins_path: Path) -> None:
    product_rows: list[dict[str, int | str]] = [
        {
            "slot": product.slot,
            "name": product.name,
            "price_cents": product.price_cents,
            "quantity": product.quantity,
        }
        for product in state.products.values()
    ]
    coin_rows: list[dict[str, int | str]] = [
        {"coin_cents": coin, "count": count}
        for coin, count in sorted(state.coin_float.items(), reverse=True)
    ]
    _write_csv(products_path, PRODUCT_COLUMNS, product_rows)
    _write_csv(coins_path, COIN_COLUMNS, coin_rows)


def _write_csv(path: Path, columns: list[str], rows: list[dict[str, int | str]]) -> None:
    """Write to a temporary file first, so a crash never leaves a half-written CSV."""
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)
