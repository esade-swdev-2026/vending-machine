import typer

from vending_machine.formatting import format_cents, format_product_lines
from vending_machine.inventory import affordable_products
from vending_machine.machine import sell
from vending_machine.models import VendingError
from vending_machine.payment import credit_from_coins
from vending_machine.storage import read_coin_float, read_products

app = typer.Typer(help="A vending machine")


# @app.command() -->              #ver que hacemos con ella pq requiere de otra class
# def display_budget(currency: str = "€", amount_cents: int = 0) -> None:
# try:
#  message = format_budget_message(currency, amount_cents)
# typer.echo(message)
# except ValueError as error:
# typer.echo(str(error), err=True)
# raise typer.Exit(code=1) from error


def fail(error: Exception) -> typer.Exit:
    typer.echo(f"Error: {error}", err=True)
    return typer.Exit(code=1)


@app.callback()
def main() -> None:
    """A vending machine."""


@app.command()
def products(stock: str) -> None:
    try:
        for line in format_product_lines(read_products(stock)):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error


@app.command()
def affordable(stock: str, coins: list[int]) -> None:
    try:
        credit = credit_from_coins(coins)
        typer.echo(f"Credit: {format_cents(credit)}")
        for line in format_product_lines(affordable_products(read_products(stock), credit)):
            typer.echo(line)
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error


@app.command()
def buy(stock: str, coins_file: str, slot: int, coins: list[int]) -> None:
    try:
        sale = sell(read_products(stock), slot, coins, read_coin_float(coins_file))
        typer.echo(f"Enjoy your {sale.product.product_name}!")
        change = format_cents(sum(sale.change))
        typer.echo(f"Change: {change}")
    except (VendingError, OSError, ValueError) as error:
        raise fail(error) from error
