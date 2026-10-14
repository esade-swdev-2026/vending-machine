from dataclasses import dataclass


@dataclass (frozen=True)
class ProductDetails:
    quantity: int
    price: float
