from vending_machine.inventory import find_product
from vending_machine.models import InsufficientCredit, Product, Sale, SoldOut
from vending_machine.payment import credit_from_coins, make_change


def sell(products: list[Product], slot: int, coins: list[int], coin_float: dict[int, int]) -> Sale:
    product = find_product(products, slot)
    if product.quantity == 0:
        raise SoldOut(f"{product.name} is sold out.")
    credit = credit_from_coins(coins)
    if credit < product.price_cents:
        raise InsufficientCredit(
            f"{product.name} costs {product.price_cents} cents, you inserted {credit}."
        )
    change = make_change(credit - product.price_cents, coin_float)
    return Sale(product, change)
