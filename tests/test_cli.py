import shutil
from pathlib import Path

from typer.testing import CliRunner

from vending_machine.cli import app

runner = CliRunner()
DATA = Path(__file__).parent.parent / "data"


def copy_data_files(folder: Path) -> list[str]:
    """buy saves the new stock, so each test works on its own copy of the data files."""
    stock = shutil.copy(DATA / "products.csv", folder / "products.csv")
    coins = shutil.copy(DATA / "machine_coins_change.csv", folder / "machine_coins_change.csv")
    return ["--stock", str(stock), "--coins-file", str(coins)]


def test_buy_prints_product_and_change(tmp_path: Path) -> None:
    result = runner.invoke(app, ["buy", "2", "200", *copy_data_files(tmp_path)])
    assert result.exit_code == 0
    assert "KitKat" in result.output
    assert "1 x 0.50 € + 1 x 0.20 €" in result.output


def test_buy_saves_the_new_stock(tmp_path: Path) -> None:
    files = copy_data_files(tmp_path)
    runner.invoke(app, ["buy", "2", "200", *files])
    assert "2,KitKat,130,4" in (tmp_path / "products.csv").read_text(encoding="utf-8")


def test_buy_unknown_slot_exits_with_error_and_saves_nothing(tmp_path: Path) -> None:
    files = copy_data_files(tmp_path)
    before = (tmp_path / "products.csv").read_text(encoding="utf-8")
    result = runner.invoke(app, ["buy", "99", "200", *files])
    assert result.exit_code == 1
    assert "Error:" in result.output
    assert (tmp_path / "products.csv").read_text(encoding="utf-8") == before
