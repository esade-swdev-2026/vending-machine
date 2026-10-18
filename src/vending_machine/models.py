from dataclasses import dataclass

ACCEPTED_COINS_CENTS: tuple[int, ...] = (200, 100, 50, 20, 10, 5, 2, 1)


@dataclass(frozen=True)
class Product:
    slot: int
    name: str
    price_cents: int
    quantity: int


@dataclass(frozen=True)
class Sale:
    product: Product
    change: list[int]


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
