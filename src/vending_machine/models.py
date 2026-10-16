from dataclasses import dataclass

ACCEPTED_COINS_CENTS: list[int] = [200, 100, 50, 20, 10, 5, 2, 1]


@dataclass(frozen=True)
class Product:
    slot: int
    product_name: str
    quantity: int
    price_cents: int


@dataclass(frozen=True)
class Sale:
    product: Product
    change: list[int]


# add error classes(VendingError):
# UnknownSlot, SoldOut, InvalidCoin, InsufficientCredit, CannotMakeChange. --> REVIEW


class VendingError(Exception):
    """Base class for every vending machine failure."""


class UnknownSlot(VendingError):
    pass


class SoldOut(VendingError):
    pass


class InvalidCoin(VendingError):
    pass


class InsufficientCredit(VendingError):
    pass


class CannotMakeChange(VendingError):
    pass
