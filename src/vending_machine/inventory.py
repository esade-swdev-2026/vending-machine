from dataclasses import replace

from vending_machine.models import InvalidQuantity, Product, Products, UnknownSlot

MAX_UNITS_PER_SLOT = 20


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


def restock_slot(products: Products, slot: int, units_added: int) -> Products:
    product = find_product(products, slot)
    if units_added <= 0:
        raise InvalidQuantity("Restock at least 1 unit.")
    new_quantity = product.quantity + units_added
    if new_quantity > MAX_UNITS_PER_SLOT:
        raise InvalidQuantity(
            f"Slot {slot} holds at most {MAX_UNITS_PER_SLOT} units; it has {product.quantity}."
        )
    return {**products, slot: replace(product, quantity=product.quantity + units_added)}
