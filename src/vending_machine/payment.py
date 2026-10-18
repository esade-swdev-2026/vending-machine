from vending_machine.models import ACCEPTED_COINS_CENTS, CannotMakeChange, InvalidCoin


def credit_from_coins(coins: list[int]) -> int:
    for coin in coins:
        if coin not in ACCEPTED_COINS_CENTS:
            raise InvalidCoin(f"Coin {coin} is not accepted.")
    return sum(coins)


def make_change(amount_cents: int, coin_float: dict[int, int]) -> list[int]:
    change = []
    remaining = amount_cents
    for coin in sorted(coin_float, reverse=True):
        count = min(remaining // coin, coin_float[coin])
        change.extend([coin] * count)
        remaining -= coin * count
    if remaining > 0:
        raise CannotMakeChange(f"Cannot give {remaining} cents of change.")
    return change
