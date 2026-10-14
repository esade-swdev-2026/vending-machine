import typer

from vending_machine.formatting import format_budget_message

app = typer.Typer(help="A vending machine")


@app.callback()
def main() -> None:
    """A vending machine."""


@app.command()
def display_budget(currency: str, amount: float = 0) -> None:
    try:
        message = format_budget_message(currency, amount)
        typer.echo(message)
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
