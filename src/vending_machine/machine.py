from dataclasses import replace

from vending_machine.inventory import find_product
from vending_machine.models import (
    Coins,
    InsufficientCredit,
    MachineState,
    Sale,
    SaleResult,
    SoldOut,
)
from vending_machine.payment import add_coins, credit_from_coins, make_change, remove_coins


def sell(state: MachineState, slot: int, coins: Coins) -> SaleResult:
    product = find_product(state.products, slot)
    if product.quantity == 0:
        raise SoldOut(f"{product.name} is sold out.")
    credit = credit_from_coins(coins)
    if credit < product.price_cents:
        raise InsufficientCredit(
            f"{product.name} costs {product.price_cents} cents, you inserted {credit}."
        )
    coins_in_machine = add_coins(state.coin_float, coins)
    change = make_change(credit - product.price_cents, coins_in_machine)
    new_state = MachineState(
        products={**state.products, slot: replace(product, quantity=product.quantity - 1)},
        coin_float=remove_coins(coins_in_machine, change),
    )
    return SaleResult(Sale(product, change), new_state)
