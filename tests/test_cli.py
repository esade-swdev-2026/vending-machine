from pathlib import Path

from typer.testing import CliRunner

from vending_machine.cli import app

runner = CliRunner()

PRODUCTS_CSV = "slot,name,price_cents,quantity\n1,Choco bons,150,10\n2,KitKat,130,5\n"
COINS_CSV = "coin_cents,count\n200,5\n100,10\n50,10\n20,10\n10,10\n5,10\n"


def write_data_files(folder: Path) -> list[str]:
    stock = folder / "products.csv"
    coins = folder / "machine_coins_change.csv"
    stock.write_text(PRODUCTS_CSV, encoding="utf-8")
    coins.write_text(COINS_CSV, encoding="utf-8")
    return ["--stock", str(stock), "--coins-file", str(coins)]


def test_buy_prints_product_and_change(tmp_path: Path) -> None:
    result = runner.invoke(app, ["buy", "2", "200", *write_data_files(tmp_path)])
    assert result.exit_code == 0
    assert "KitKat" in result.output
    assert "1 x 0.50 € + 1 x 0.20 €" in result.output


def test_buy_saves_the_new_stock(tmp_path: Path) -> None:
    files = write_data_files(tmp_path)
    runner.invoke(app, ["buy", "2", "200", *files])
    assert "2,KitKat,130,4" in (tmp_path / "products.csv").read_text(encoding="utf-8")


def test_buy_unknown_slot_exits_with_error_and_saves_nothing(tmp_path: Path) -> None:
    files = write_data_files(tmp_path)
    before = (tmp_path / "products.csv").read_text(encoding="utf-8")
    result = runner.invoke(app, ["buy", "99", "200", *files])
    assert result.exit_code == 1
    assert "Error:" in result.output
    assert (tmp_path / "products.csv").read_text(encoding="utf-8") == before


def test_help_describes_every_command() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "List every product" in result.output
    assert "Buy the product" in result.output


def test_refill_lists_only_the_empty_slots(tmp_path: Path) -> None:
    stock = tmp_path / "products.csv"
    stock.write_text(
        "slot,name,price_cents,quantity\n1,KitKat,130,5\n3,Kinder Bueno,180,0\n", encoding="utf-8"
    )
    result = runner.invoke(app, ["refill", "--stock", str(stock)])
    assert result.exit_code == 0
    assert "1 slot(s) to refill:" in result.output
    assert "Kinder Bueno" in result.output
    assert "KitKat" not in result.output


def test_refill_says_when_nothing_is_empty(tmp_path: Path) -> None:
    stock = tmp_path / "products.csv"
    stock.write_text("slot,name,price_cents,quantity\n1,KitKat,130,5\n", encoding="utf-8")
    result = runner.invoke(app, ["refill", "--stock", str(stock)])
    assert result.exit_code == 0
    assert "Nothing to refill" in result.output
