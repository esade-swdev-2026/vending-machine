import vending_machine.formatting
from vending_machine.inventory import find_product_for_slot
from vending_machine.models import InsufficientCredit, Product, Sale, SoldOut
from vending_machine.payment import credit_from_coins, make_change


def sell(
    products: list[Product], slot: int, coins: list[int], coin_float: dict[int, int]
) -> Sale:  # cambiar al hacer dict  # noqa: E501
    product = find_product_for_slot(products, slot)
    if product.quantity == 0:
        raise SoldOut(f"{product.product_name} is sold out.")
    credit = credit_from_coins(coins)
    if credit < product.price_cents:
        raise InsufficientCredit(
            f"{product.product_name} costs {vending_machine.formatting.format_cents(product.price_cents)}, you inserted {vending_machine.formatting.format_cents(credit)} ."  # noqa: E501
        )
    change = make_change(credit - product.price_cents, coin_float)
    return Sale(product, change)
