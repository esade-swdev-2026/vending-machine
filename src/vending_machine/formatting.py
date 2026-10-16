def format_budget_message(currency: str = "€", amount: float = 0) -> str:
    if amount < 0:
        raise ValueError("Invalid amount.")
    return f"Your current balance is: {amount:.2f}{currency}"

#remove format budget message and replace with format_cents (lo que dijo masde deponer todo encents)
#funcion format_product_lines, para poner los precios y los sold outs a los productos
#cambia los objectos en lineas de texto listas para ser printeadas. 


