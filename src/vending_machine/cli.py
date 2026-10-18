from collections import Counter
from pathlib import Path
from typing import Annotated

import typer

from vending_machine.formatting import format_cents, format_change, format_product_lines
from vending_machine.inventory import affordable_products
from vending_machine.machine import sell
from vending_machine.models import VendingError
from vending_machine.payment import credit_from_coins
from vending_machine.storage import read_products, read_state, write_state

app = typer.Typer(help="A vending machine")

StockOption = Annotated[Path, typer.Option("--stock", help="Products CSV file.")]
CoinsFileOption = Annotated[Path, typer.Option("--coins-file", help="Coin float CSV file.")]
CoinsArgument = Annotated[list[int], typer.Argument(help="Inserted coins, in cents.")]

DEFAULT_STOCK = Path("data/products.csv")
DEFAULT_COINS_FILE = Path("data/machine_coins_change.csv")


def fail(error: Exception) -> typer.Exit:
    typer.echo(f"Error: {error}", err=True)
    return typer.Exit(code=1)


@app.callback()
def main() -> None:
    """A vending machine."""


@app.command()
def products(
    stock: StockOption = DEFAULT_STOCK, coins_file: CoinsFileOption = DEFAULT_COINS_FILE
) -> None:
    try:
        for line in format_product_lines(list(read_products(stock).values())):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error


@app.command()
def affordable(
    coins: CoinsArgument,
    stock: StockOption = DEFAULT_STOCK,
    coins_file: CoinsFileOption = DEFAULT_COINS_FILE,
) -> None:
    try:
        credit = credit_from_coins(Counter(coins))
        typer.echo(f"Credit: {format_cents(credit)}")
        for line in format_product_lines(affordable_products(read_products(stock), credit)):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error


@app.command()
def buy(
    slot: int,
    coins: CoinsArgument,
    stock: StockOption = DEFAULT_STOCK,
    coins_file: CoinsFileOption = DEFAULT_COINS_FILE,
) -> None:
    try:
        result = sell(read_state(stock, coins_file), slot, Counter(coins))
        write_state(result.state, stock, coins_file)
        typer.echo(f"Enjoy your {result.sale.product.name}!")
        typer.echo(f"Change: {format_change(result.sale.change)}")
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error
