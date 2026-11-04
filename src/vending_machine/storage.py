import csv
from pathlib import Path

from vending_machine.models import ACCEPTED_COINS_CENTS, Coins, MachineState, Product, Products

PRODUCT_COLUMNS = ["slot", "name", "price_cents", "quantity"]
COIN_COLUMNS = ["coin_cents", "count"]
FIRST_DATA_LINE = 2
REVENUE_COLUMNS = ["revenue_cents"]


def read_products(path: Path) -> Products:
    _check_file_exists(path)
    products: Products = {}
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=FIRST_DATA_LINE):
            try:
                product = Product(
                    slot=int(row["slot"]),
                    name=row["name"],
                    price_cents=int(row["price_cents"]),
                    quantity=int(row["quantity"]),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad product on line {line_number}.") from error
            if product.price_cents <= 0:
                raise ValueError(f"{path}: price must be more than 0 on line {line_number}.")
            if product.quantity < 0:
                raise ValueError(f"{path}: quantity cannot be negative on line {line_number}.")
            if product.slot in products:
                raise ValueError(f"{path}: slot {product.slot} is repeated on line {line_number}.")
            products[product.slot] = product
    return products


def read_coin_float(path: Path) -> Coins:
    _check_file_exists(path)
    coin_float: Coins = {}
    with path.open(newline="", encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=FIRST_DATA_LINE):
            try:
                coin, count = int(row["coin_cents"]), int(row["count"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"{path}: bad coin on line {line_number}.") from error
            if coin not in ACCEPTED_COINS_CENTS:
                raise ValueError(f"{path}: coin {coin} is not accepted on line {line_number}.")
            if count < 0:
                raise ValueError(f"{path}: coin count cannot be negative on line {line_number}.")
            coin_float[coin] = count
    return coin_float


def read_revenue(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    if len(rows) != 1:
        raise ValueError(f"{path}: expected exactly one revenue row.")
    try:
        revenue = int(rows[0]["revenue_cents"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"{path}: invalid revenue.") from error
    if revenue < 0:
        raise ValueError(f"{path}: revenue cannot be negative.")
    return revenue


def write_revenue(path: Path, revenue_cents: int) -> None:
    if revenue_cents < 0:
        raise ValueError("Revenue cannot be negative.")

    _write_csv(
        path,
        REVENUE_COLUMNS,
        [{"revenue_cents": revenue_cents}],
    )


def read_state(
    products_path: Path, coins_path: Path, revenue_path: Path | None = None
) -> MachineState:
    if revenue_path is None:
        revenue_path = products_path.with_name("revenue.csv")
    return MachineState(
        read_products(products_path), read_coin_float(coins_path), read_revenue(revenue_path)
    )


def write_state(
    state: MachineState, products_path: Path, coins_path: Path, revenue_path: Path | None = None
) -> None:
    if revenue_path is None:
        revenue_path = products_path.with_name("revenue.csv")
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
    write_revenue(revenue_path, state.revenue_cents)


def _check_file_exists(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{path} not found. Run from the repository root.")


def _write_csv(path: Path, columns: list[str], rows: list[dict[str, int | str]]) -> None:
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)
