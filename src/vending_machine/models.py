from dataclasses import dataclass

ACCEPTED_COINS_CENTS: tuple[int, ...] = (200, 100, 50, 20, 10, 5, 2, 1)

Coins = dict[int, int]
"""A handful of coins: coin value in cents -> how many of that coin."""


@dataclass(frozen=True)
class Product:
    slot: int
    name: str
    price_cents: int
    quantity: int


Products = dict[int, Product]
"""Every product in the machine, keyed by its slot number."""


@dataclass(frozen=True)
class Sale:
    product: Product
    change: Coins


@dataclass(frozen=True)
class MachineState:
    """Everything the machine holds: its products and the coins it can give as change."""

    products: Products
    coin_float: Coins


@dataclass(frozen=True)
class SaleResult:
    """What one sale gives back: the sale itself and the machine as it is after the sale."""

    sale: Sale
    state: MachineState


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
