import pandas as pd

from vending_machine.models import Product


def read_products(path: str) -> list[Product]:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    products = []
    for i in range(len(df)):
        try:
            product = Product(
                slot=int(df["slot"].iloc[i]),
                name=str(df["name"].iloc[i]),
                price_cents=int(df["price_cents"].iloc[i]),
                quantity=int(df["quantity"].iloc[i]),
            )
            products.append(product)
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{path}: bad product on line {i + 2}.") from error
    return products


def read_coin_float(path: str) -> dict[int, int]:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    coin_float = {}
    for i in range(len(df)):
        try:
            coin_float[int(df["coin_cents"].iloc[i])] = int(df["count"].iloc[i])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"{path}: bad coin on line {i + 2}.") from error
    return coin_float
