from vending_machine.models import Product, Products, UnknownSlot


def find_product(products: Products, slot: int) -> Product:
    try:
        return products[slot]
    except KeyError:
        raise UnknownSlot(f"No product in slot {slot}.") from None


def affordable_products(products: Products, credit_cents: int) -> list[Product]:
    return [p for p in products.values() if p.quantity > 0 and p.price_cents <= credit_cents]
