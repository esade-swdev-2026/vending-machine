from vending_machine.models import Product, UnknownSlot


def find_product(products: list[Product], slot: int) -> Product:
    for product in products:
        if product.slot == slot:
            return product
    raise UnknownSlot(f"No product in slot {slot}.")


def affordable_products(products: list[Product], credit_cents: int) -> list[Product]:
    return [p for p in products if p.quantity > 0 and p.price_cents <= credit_cents]
