"""Tests that execute every statement in the shopping cart application."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    "category, price, qty, expected",
    [
        ("food", 100, 2, 210),
        ("electronics", 100, 10, 1062),
        ("clothing", 100, 1, 112),
    ],
)
def test_item_total(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


def test_unknown_category():
    with pytest.raises(ValueError, match="^unknown category$"):
        item_total("books", 100, 1)


@pytest.mark.parametrize("price, qty", [(-1, 1), (100, 0)])
def test_invalid_item(price, qty):
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", price, qty)


@pytest.mark.parametrize(
    "cart_value, expected", [(5000, 1100), (2000, 500), (1000, 200)]
)
def test_cart_discount_tiers(cart_value, expected):
    assert cart_discount(cart_value, True, "FLAT10") == expected


@pytest.mark.parametrize(
    "cart_value, is_prime, expected",
    [(0, True, 50), (500, False, 100), (499, False, 140)],
)
def test_express_shipping(cart_value, is_prime, expected):
    assert shipping_fee(cart_value, is_prime, True) == expected
