"""Independent branch, boundary, and error-path tests for Lab 6."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    "category, price, qty, expected",
    [
        ("food", 100, 2, 210),
        ("electronics", 100, 2, 236),
        ("clothing", 100, 2, 224),
        ("food", 100, 9, 945),       # Below the bulk threshold.
        ("food", 100, 10, 945),      # Bulk discount starts here.
        ("food", 100, 11, 1039),     # GST uses integer division.
        ("electronics", 100, 10, 1062),
        ("electronics", 123, 3, 435),
        ("food", 1, 11, 10),
        ("clothing", 0, 1, 0),       # Zero price is valid.
        ("clothing", 0, 10, 0),
    ],
)
def test_item_categories_bulk_boundary_and_rounding(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


@pytest.mark.parametrize("category", ["books", "", "Food"])
def test_unknown_categories(category):
    with pytest.raises(ValueError, match="^unknown category$"):
        item_total(category, 100, 1)


@pytest.mark.parametrize("price, qty", [(-1, 1), (100, 0), (100, -1), (-1, 0)])
def test_invalid_prices_and_quantities(price, qty):
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", price, qty)


@pytest.mark.parametrize(
    "cart_value, is_prime, coupon, expected",
    [
        (0, False, None, 0),
        (999, False, "FLAT10", 0),
        (1000, False, "FLAT10", 100),
        (1001, False, "FLAT10", 100),
        (1999, False, None, 0),
        (2000, False, None, 200),
        (2001, False, None, 200),
        (4999, False, None, 200),
        (5000, False, None, 500),
        (5001, False, None, 500),
        (0, True, None, 100),
        (2000, True, None, 300),
        (5000, True, None, 600),
        (999, True, "FLAT10", 100),
        (1000, True, "FLAT10", 200),
        (1999, False, "FLAT10", 199),
        (2000, False, "FLAT10", 400),
        (2000, True, "FLAT10", 500),
        (4999, False, "FLAT10", 699),
        (5000, False, "FLAT10", 1000),
        (5000, True, "FLAT10", 1100),
        (5001, True, "FLAT10", 1100),
        (1000, False, "OTHER", 0),
        (1000, False, "flat10", 0),
        (5000, True, "", 600),
    ],
)
def test_discount_tiers_prime_coupon_and_boundaries(
    cart_value, is_prime, coupon, expected
):
    assert cart_discount(cart_value, is_prime, coupon) == expected


@pytest.mark.parametrize(
    "cart_value, is_prime, is_express, expected",
    [
        (0, False, False, 40),
        (0, False, True, 140),
        (0, True, False, 0),
        (0, True, True, 50),
        (499, False, False, 40),
        (499, False, True, 140),
        (499, True, False, 0),
        (499, True, True, 50),
        (500, False, False, 0),
        (500, False, True, 100),
        (500, True, False, 0),
        (500, True, True, 50),
        (501, False, False, 0),
        (501, False, True, 100),
        (501, True, False, 0),
        (501, True, True, 50),
        (1000, False, False, 0),     # Original free-shipping example.
    ],
)
def test_shipping_threshold_prime_and_express(
    cart_value, is_prime, is_express, expected
):
    assert shipping_fee(cart_value, is_prime, is_express) == expected
