from dataclasses import dataclass


@dataclass(frozen=True)
class ProductDetails:
    product_name: str
    slot: int               
    quantity: int           
    price: float            

                            
#rename ProductDetails to Product (Clean Code)
#replace vafriables with: slot, name, price_cents, quantity
#add one @dataclass called Sale
#add error classes(VendingError):
#UnknownSlot, SoldOut, InvalidCoin, InsufficientCredit, CannotMakeChange.

