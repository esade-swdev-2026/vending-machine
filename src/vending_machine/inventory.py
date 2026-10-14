from vending_machine.models import ProductDetails


def get_possible_products_by_budget(
    products_in_machine: dict[str, ProductDetails], 
    budget: float = 0
) -> list[str]:
    available = []
    for product, details in products_in_machine.items():
        if details.quantity > 0 and details.price <= budget:
            available.append(product)
    return available
