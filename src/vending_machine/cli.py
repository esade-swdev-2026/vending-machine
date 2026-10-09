from dataclasses import dataclass

import typer

app = typer.Typer(help="A vending machine")

@dataclass
class Products_details:
    quantity: int
    price: float


@app.callback()
def main() -> None:
    """A vending machine."""


def format_budget_message(currency: str, amount: float) -> str:
    if amount < 0:
        raise ValueError("Invalid amount.")
    return f"Your current balance is: {amount:.2f}{currency}"

@app.command()
def display_budget(currency: str, amount: float = 0) -> None:
    try:
        message = format_budget_message(currency, amount)
        typer.echo(message)
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1) from e


def display_possible_products_by_budget(
    products_in_machine: dict[str, Products_details], 
    budget: float = 0
) -> list[str]:
    available = []
    for product,details in products_in_machine.items():
        if details.quantity > 0 and details.price <= budget:
            available.append(product)
    return available


if __name__ == "__main__":
    app()
