from collections import Counter
from dataclasses import replace
from pathlib import Path
from typing import Annotated, NoReturn

import typer

from vending_machine.formatting import format_cents, format_change, format_product_lines
from vending_machine.inventory import affordable_products, empty_slots, restock_slot
from vending_machine.machine import sell
from vending_machine.models import VendingError
from vending_machine.payment import credit_from_coins
from vending_machine.storage import (
    read_products,
    read_revenue,
    read_state,
    write_revenue,
    write_state,
)

app = typer.Typer(help="A terminal vending machine that sells products and gives change.")

StockOption = Annotated[Path, typer.Option("--stock", help="Products CSV file.")]
CoinsFileOption = Annotated[Path, typer.Option("--coins-file", help="Coin float CSV file.")]
RevenueFileOption = Annotated[
    Path,
    typer.Option("--revenue-file", help="Session revenue CSV file."),
]
CoinsArgument = Annotated[list[int], typer.Argument(help="Inserted coins, in cents.")]
SlotArgument = Annotated[int, typer.Argument(help="Slot number of the product to buy.")]
RestockSlotArgument = Annotated[int, typer.Argument(help="Slot number to restock.")]
UnitsArgument = Annotated[int, typer.Argument(help="Units to add to the slot.")]

DEFAULT_STOCK = Path("data/products.csv")
DEFAULT_COINS_FILE = Path("data/machine_coins_change.csv")
DEFAULT_REVENUE_FILE = Path("data/revenue.csv")


def exit_with_error(error: Exception) -> NoReturn:
    typer.echo(f"Error: {error}", err=True)
    raise typer.Exit(code=1) from error


@app.callback()
def main() -> None:
    """A terminal vending machine that sells products and gives change."""


@app.command()
def products(stock: StockOption = DEFAULT_STOCK) -> None:
    """List every product with its slot and price, or SOLD OUT."""
    try:
        for line in format_product_lines(list(read_products(stock).values())):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        exit_with_error(error)


@app.command()
def affordable(coins: CoinsArgument, stock: StockOption = DEFAULT_STOCK) -> None:
    """Show your credit and the products you can buy with these coins."""
    try:
        credit = credit_from_coins(Counter(coins))
        typer.echo(f"Credit: {format_cents(credit)}")
        for line in format_product_lines(affordable_products(read_products(stock), credit)):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        exit_with_error(error)


@app.command()
def buy(
    slot: SlotArgument,
    coins: CoinsArgument,
    stock: StockOption = DEFAULT_STOCK,
    coins_file: CoinsFileOption = DEFAULT_COINS_FILE,
    revenue_file: RevenueFileOption = DEFAULT_REVENUE_FILE,
) -> None:
    """Buy the product in SLOT with COINS, get your change, and save the machine."""
    try:
        result = sell(read_state(stock, coins_file, revenue_file), slot, Counter(coins))
        write_state(result.state, stock, coins_file, revenue_file)
        typer.echo(f"Enjoy your {result.sale.product.name}!")
        typer.echo(f"Change: {format_change(result.sale.change)}")
    except (VendingError, OSError, ValueError) as error:
        exit_with_error(error)


@app.command()
def restock(
    slot: RestockSlotArgument,
    units: UnitsArgument,
    stock: StockOption = DEFAULT_STOCK,
    coins_file: CoinsFileOption = DEFAULT_COINS_FILE,
    revenue_file: RevenueFileOption = DEFAULT_REVENUE_FILE,
) -> None:
    """For the owner: add UNITS to the product in SLOT and save the stock."""
    try:
        state = read_state(stock, coins_file, revenue_file)
        new_state = replace(state, products=restock_slot(state.products, slot, units))
        write_state(new_state, stock, coins_file, revenue_file)
    except (VendingError, OSError, ValueError) as error:
        exit_with_error(error)
    product = new_state.products[slot]
    typer.echo(f"Slot {slot}: {product.name} now has {product.quantity} units.")


@app.command()
def refill(stock: StockOption = DEFAULT_STOCK) -> None:
    """For the owner: list the empty slots that need a refill."""
    try:
        slots_to_refill = empty_slots(read_products(stock))
    except (VendingError, OSError, ValueError) as error:
        exit_with_error(error)
    if not slots_to_refill:
        typer.echo("Every slot has stock. Nothing to refill.")
        return
    typer.echo(f"{len(slots_to_refill)} slot(s) to refill:")
    for line in format_product_lines(slots_to_refill):
        typer.echo(line)


@app.command()
def revenue(revenue_file: RevenueFileOption = DEFAULT_REVENUE_FILE) -> None:
    """For the owner: show the current session revenue."""
    try:
        total_cents = read_revenue(revenue_file)
        typer.echo(f"Current session revenue: {format_cents(total_cents)}")
    except (OSError, ValueError) as error:
        exit_with_error(error)


@app.command()
def start_session(
    revenue_file: RevenueFileOption = DEFAULT_REVENUE_FILE,
) -> None:
    """For the owner: start a new session with zero revenue."""
    try:
        write_revenue(revenue_file, 0)
        typer.echo(f"New session started. Revenue: {format_cents(0)}")
    except (OSError, ValueError) as error:
        exit_with_error(error)
