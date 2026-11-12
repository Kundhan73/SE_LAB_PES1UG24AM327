import re


ZONES = {
    "1": "North", "2": "North", "3": "West", "4": "West",
    "5": "South", "6": "South", "7": "East", "8": "East",
}

CART_ITEM = re.compile(r"([^,:\r\n]+):([0-9]+)x([0-9]+)")
PROMO_CODE = re.compile(r"OFF([0-9]+)", re.IGNORECASE)
PINCODE = re.compile(r"[0-9]{6}")


def cart_total(cart):
    """Return the total for a valid cart, or None for invalid input."""
    if not isinstance(cart, str):
        return None

    total = 0
    try:
        for item in cart.split(","):
            match = CART_ITEM.fullmatch(item.strip())
            if match is None or not match[1].strip():
                return None
            price, quantity = int(match[2]), int(match[3])
            total += price * quantity
        str(total)  # Check that the CLI can display the total within Python's digit limit.
    except ValueError:
        return None
    return total


def promo_percent(code):
    """Return a discount from 0 to 100, or None for invalid input."""
    if not isinstance(code, str):
        return None

    match = PROMO_CODE.fullmatch(code.strip())
    if match is None:
        return None

    digits = match[1].lstrip("0")
    if len(digits) > 3:
        return None
    percent = int(digits or "0")
    return percent if percent <= 100 else None


def delivery_zone(pincode):
    """Return the zone of a supported six-digit pincode, or None."""
    if not isinstance(pincode, str):
        return None

    pincode = pincode.strip()
    if PINCODE.fullmatch(pincode) is None:
        return None
    return ZONES.get(pincode[0])


def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    if result is None:
        print("Invalid cart.")
    else:
        print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    if result is None:
        print("Invalid promo code.")
    else:
        print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    if result is None:
        print("Invalid pincode.")
    else:
        print("Delivery Zone:", result)


if __name__ == "__main__":
    main()
