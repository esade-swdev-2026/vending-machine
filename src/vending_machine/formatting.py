from vending_machine.models import Coins, Product

CENTS_PER_EURO = 100


def format_cents(cents: int) -> str:
    return f"{cents // CENTS_PER_EURO}.{cents % CENTS_PER_EURO:02d} €"


def format_product_lines(products: list[Product]) -> list[str]:
    lines = []
    for product in products:
        price = "SOLD OUT" if product.quantity <= 0 else format_cents(product.price_cents)
        lines.append(f"{product.slot:>3}  {product.name:<15} {price}")
    return lines


def format_change(change: Coins) -> str:
    coins = sorted(change.items(), reverse=True)
    return " + ".join(f"{count} x {format_cents(coin)}" for coin, count in coins) or "none"
