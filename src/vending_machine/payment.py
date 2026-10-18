from vending_machine.models import ACCEPTED_COINS_CENTS, CannotMakeChange, Coins, InvalidCoin


def credit_from_coins(coins: Coins) -> int:
    for coin, count in coins.items():
        if coin not in ACCEPTED_COINS_CENTS:
            raise InvalidCoin(f"Coin {coin} is not accepted.")
        if count < 0:
            raise InvalidCoin(f"Cannot insert {count} coins of {coin}.")
    return sum(coin * count for coin, count in coins.items())


def add_coins(first: Coins, second: Coins) -> Coins:
    return {coin: first.get(coin, 0) + second.get(coin, 0) for coin in first | second}


def remove_coins(coins: Coins, taken: Coins) -> Coins:
    return {coin: count - taken.get(coin, 0) for coin, count in coins.items()}


def make_change(amount_cents: int, coin_float: Coins) -> Coins:
    change = _find_change(amount_cents, sorted(coin_float, reverse=True), coin_float)
    if change is None:
        raise CannotMakeChange(f"Cannot give {amount_cents} cents of change.")
    return change


def _find_change(amount_cents: int, coins: list[int], coin_float: Coins) -> Coins | None:
    """Try as many of the biggest coin as possible; if the rest cannot be paid, use one fewer."""
    if amount_cents == 0:
        return {}
    if not coins:
        return None
    coin, smaller_coins = coins[0], coins[1:]
    most = min(amount_cents // coin, coin_float[coin])
    for count in range(most, -1, -1):
        rest = _find_change(amount_cents - coin * count, smaller_coins, coin_float)
        if rest is not None:
            return {coin: count, **rest} if count > 0 else rest
    return None
