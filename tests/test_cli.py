from pathlib import Path

import pytest
from typer.testing import CliRunner

from vending_machine.cli import app
from vending_machine.storage import read_revenue

runner = CliRunner()

PRODUCTS_CSV = "slot,name,price_cents,quantity\n1,Choco bons,150,10\n2,KitKat,130,5\n"
COINS_CSV = "coin_cents,count\n200,5\n100,10\n50,10\n20,10\n10,10\n5,10\n"


def write_data_files(folder: Path) -> list[str]:
    stock = folder / "products.csv"
    coins = folder / "machine_coins_change.csv"
    revenue = folder / "revenue.csv"
    stock.write_text(PRODUCTS_CSV, encoding="utf-8")
    coins.write_text(COINS_CSV, encoding="utf-8")
    revenue.write_text("revenue_cents\n0\n", encoding="utf-8")
    return [
        "--stock",
        str(stock),
        "--coins-file",
        str(coins),
        "--revenue-file",
        str(revenue),
    ]


def test_buy_prints_product_and_change(tmp_path: Path) -> None:
    result = runner.invoke(app, ["buy", "2", "200", *write_data_files(tmp_path)])
    assert result.exit_code == 0
    assert "KitKat" in result.output
    assert "1 x 0.50 € + 1 x 0.20 €" in result.output


def test_buy_saves_the_new_stock(tmp_path: Path) -> None:
    files = write_data_files(tmp_path)
    runner.invoke(app, ["buy", "2", "200", *files])
    assert "2,KitKat,130,4" in (tmp_path / "products.csv").read_text(encoding="utf-8")


def test_buy_unknown_slot_exits_with_error_and_saves_nothing(
    tmp_path: Path,
) -> None:
    files = write_data_files(tmp_path)
    products_path = tmp_path / "products.csv"
    revenue_path = tmp_path / "revenue.csv"
    revenue_path.write_text(
        "revenue_cents\n620\n",
        encoding="utf-8",
    )
    products_before = products_path.read_text(encoding="utf-8")
    revenue_before = revenue_path.read_text(encoding="utf-8")
    result = runner.invoke(app, ["buy", "99", "200", *files])
    assert result.exit_code == 1
    assert "Error:" in result.output
    assert products_path.read_text(encoding="utf-8") == products_before
    assert revenue_path.read_text(encoding="utf-8") == revenue_before
    assert read_revenue(revenue_path) == 620


def test_restock_saves_the_new_quantity(tmp_path: Path) -> None:
    result = runner.invoke(app, ["restock", "2", "3", *write_data_files(tmp_path)])
    assert result.exit_code == 0
    assert "Slot 2: KitKat now has 8 units." in result.output
    assert "2,KitKat,130,8" in (tmp_path / "products.csv").read_text(encoding="utf-8")


def test_restock_unknown_slot_exits_with_error_and_saves_nothing(tmp_path: Path) -> None:
    files = write_data_files(tmp_path)
    before = (tmp_path / "products.csv").read_text(encoding="utf-8")
    result = runner.invoke(app, ["restock", "99", "3", *files])
    assert result.exit_code == 1
    assert "Error: No product in slot 99." in result.output
    assert (tmp_path / "products.csv").read_text(encoding="utf-8") == before


@pytest.mark.parametrize("bad_units", ["0", "-3", "99"])
def test_restock_invalid_quantity_exits_with_error_and_saves_nothing(
    tmp_path: Path, bad_units: str
) -> None:
    files = write_data_files(tmp_path)
    before = (tmp_path / "products.csv").read_text(encoding="utf-8")
    result = runner.invoke(app, ["restock", *files, "--", "2", bad_units])
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


def test_revenue_command_displays_session_total(tmp_path: Path) -> None:
    revenue_file = tmp_path / "revenue.csv"
    revenue_file.write_text(
        "revenue_cents\n250\n",
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["revenue", "--revenue-file", str(revenue_file)],
    )
    assert result.exit_code == 0
    assert "Current session revenue: 2.50 €" in result.output


def test_start_session_resets_revenue(tmp_path: Path) -> None:
    revenue_file = tmp_path / "revenue.csv"
    revenue_file.write_text(
        "revenue_cents\n250\n",
        encoding="utf-8",
    )
    result = runner.invoke(
        app,
        ["start-session", "--revenue-file", str(revenue_file)],
    )
    assert result.exit_code == 0
    assert read_revenue(revenue_file) == 0


def test_buy_updates_session_revenue(tmp_path: Path) -> None:
    stock = tmp_path / "products.csv"
    coins = tmp_path / "coins.csv"
    revenue_file = tmp_path / "revenue.csv"
    stock.write_text(
        "slot,name,price_cents,quantity\n1,Water,100,3\n",
        encoding="utf-8",
    )
    coins.write_text(
        "coin_cents,count\n",
        encoding="utf-8",
    )
    purchase = runner.invoke(
        app,
        [
            "buy",
            "1",
            "100",
            "--stock",
            str(stock),
            "--coins-file",
            str(coins),
            "--revenue-file",
            str(revenue_file),
        ],
    )
    assert purchase.exit_code == 0
    assert read_revenue(revenue_file) == 100
    displayed = runner.invoke(
        app,
        ["revenue", "--revenue-file", str(revenue_file)],
    )
    assert displayed.exit_code == 0
    assert "Current session revenue: 1.00 €" in displayed.output


def test_start_session_preserves_inventory_and_coins(
    tmp_path: Path,
) -> None:
    stock = tmp_path / "products.csv"
    coins = tmp_path / "coins.csv"
    revenue_file = tmp_path / "revenue.csv"

    stock.write_text(
        "slot,name,price_cents,quantity\n1,Water,100,3\n",
        encoding="utf-8",
    )
    coins.write_text(
        "coin_cents,count\n100,2\n",
        encoding="utf-8",
    )
    revenue_file.write_text(
        "revenue_cents\n250\n",
        encoding="utf-8",
    )

    original_stock = stock.read_text(encoding="utf-8")
    original_coins = coins.read_text(encoding="utf-8")

    result = runner.invoke(
        app,
        ["start-session", "--revenue-file", str(revenue_file)],
    )

    assert result.exit_code == 0
    assert read_revenue(revenue_file) == 0
    assert stock.read_text(encoding="utf-8") == original_stock
    assert coins.read_text(encoding="utf-8") == original_coins
