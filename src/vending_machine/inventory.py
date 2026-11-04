from dataclasses import replace

from vending_machine.models import Product, Products, UnknownSlot


def find_product(products: Products, slot: int) -> Product:
    try:
        return products[slot]
    except KeyError:
        raise UnknownSlot(f"No product in slot {slot}.") from None


def affordable_products(products: Products, credit_cents: int) -> list[Product]:
    return [
        product
        for product in products.values()
        if product.quantity > 0 and product.price_cents <= credit_cents
    ]


def empty_slots(products: Products) -> list[Product]:
    return [product for product in products.values() if product.quantity <= 0]


def restock_slot(products: Products, slot: int, new_units: int) -> Products:
    product = find_product(products, slot)
    if new_units <= 0:
        raise ValueError("Restock at least 1 unit.")
    return {**products, slot: replace(product, quantity=product.quantity + new_units)}
