from typer.testing import CliRunner

from vending_machine.cli import app

runner = CliRunner()


def test_add_reports_the_amount() -> None:
    result = runner.invoke(app, ["display-budget", "€", "--amount", "2.55"])
    assert result.exit_code == 0
    assert "2.55€" in result.stdout


def test_add_rejects_a_non_positive_amount() -> None:
    result = runner.invoke(app, ["display-budget", "€", "--amount", "-1"])
    assert result.exit_code == 1
