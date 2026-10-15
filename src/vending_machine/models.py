from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDetails:
    product_name: str
    slot: int
    quantity: int
    price: float
