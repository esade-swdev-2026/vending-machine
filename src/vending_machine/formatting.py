from vending_machine.models import Product


def format_cents(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}€"


def format_product_lines(products: list[Product]) -> list[str]:
    lines = []
    for product in products:
        price = "SOLD OUT" if product.quantity == 0 else format_cents(product.price_cents)
        lines.append(f"{product.slot:>3}  {product.product_name:<15} {price}")
    return lines


# remove format budget message and replace with format_cents (lo que dijo masde deponer todo encents)
# funcion format_product_lines, para poner los precios y los sold outs a los productos
# cambia los objectos en lineas de texto listas para ser printeadas.
