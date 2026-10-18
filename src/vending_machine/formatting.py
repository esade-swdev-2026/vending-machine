from vending_machine.models import Coins, Product


def format_cents(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d} €"


def format_product_lines(products: list[Product]) -> list[str]:
    lines = []
    for product in products:
        price = "SOLD OUT" if product.quantity == 0 else format_cents(product.price_cents)
        lines.append(f"{product.slot:>3}  {product.name:<15} {price}")
    return lines


def format_change(change: Coins) -> str:
    coins = sorted(change.items(), reverse=True)
    return " + ".join(f"{count} x {format_cents(coin)}" for coin, count in coins) or "none"
