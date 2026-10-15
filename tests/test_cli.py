from typer.testing import CliRunner

from vending_machine.cli import app

runner = CliRunner()


def test_cli_rejects_non_positive_amount_with_exit_code() -> None:
    result = runner.invoke(app, ["display-budget", "--currency", "$", "--amount", "-1"])
    assert result.exit_code == 1
    assert "Invalid amount." in result.output
