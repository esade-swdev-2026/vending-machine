def format_budget_message(currency: str = "€", amount: float = 0) -> str:
    if amount < 0:
        raise ValueError("Invalid amount.")
    return f"Your current balance is: {amount:.2f}{currency}"
