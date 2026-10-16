from vending_machine.models import ProductDetails


def get_possible_products_by_budget(
    products_in_machine: list[ProductDetails], budget: float = 0
) -> list[ProductDetails]:
    available = []
    for product in products_in_machine:
        if product.quantity > 0 and product.price <= budget:
            available.append(product)
    return available

#en vez de esta funcion, hacer una funcion llamada find_product y otra llamada affordable_products

