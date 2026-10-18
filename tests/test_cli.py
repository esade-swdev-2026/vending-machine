from pathlib import Path

from typer.testing import CliRunner

from vending_machine.cli import app

runner = CliRunner()
DATA = Path(__file__).parent.parent / "data"
FILES = [
    "--stock",
    str(DATA / "products.csv"),
    "--coins-file",
    str(DATA / "machine_coins_change.csv"),
]  # noqa: E501


def test_buy_prints_product_and_change() -> None:
    result = runner.invoke(app, ["buy", "2", "200", *FILES])
    assert result.exit_code == 0
    assert "KitKat" in result.output
    assert "0.50 € + 0.20 €" in result.output


def test_buy_unknown_slot_exits_with_error() -> None:
    result = runner.invoke(app, ["buy", "99", "200", *FILES])
    assert result.exit_code == 1
    assert "Error:" in result.output
