from dataclasses import dataclass

ACCEPTED_COINS_CENTS: tuple[int, ...] = (200, 100, 50, 20, 10, 5, 2, 1)

Coins = dict[int, int]


@dataclass(frozen=True)
class Product:
    slot: int
    name: str
    price_cents: int
    quantity: int


Products = dict[int, Product]


@dataclass(frozen=True)
class Sale:
    product: Product
    change: Coins


@dataclass(frozen=True)
class MachineState:
    products: Products
    coin_float: Coins


@dataclass(frozen=True)
class SaleResult:
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
