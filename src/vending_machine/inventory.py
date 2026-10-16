from vending_machine.models import Product, UnknownSlot


def find_product_for_slot(products: list[Product], slot: int) -> Product:
    for product in products:
        if product.slot == slot:
            return product
    raise UnknownSlot(f"No product in slot {slot}.")


def affordable_products(products_in_machine: list[Product], budget_cents: int = 0) -> list[Product]:
    available = []
    for product in products_in_machine:
        if product.quantity > 0 and product.price_cents <= budget_cents:
            available.append(product)
    return available
