import typer

app = typer.Typer(help="A vending machine")


@app.callback()
def main() -> None:
    """A vending machine."""


@app.command()
def display_budget(currency: str, amount: float = 0) -> None:
    if amount < 0:
        typer.echo("Unvalid amount.", err=True)
        raise typer.Exit(code=1)
    else:
        typer.echo(f"Your current balance is: {amount:.2f}{currency}")


if __name__ == "__main__":
    app()
