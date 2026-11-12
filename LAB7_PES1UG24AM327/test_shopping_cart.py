import sys

from hypothesis import given, settings, strategies as st

from shopping_cart import cart_total, delivery_zone, promo_percent


unexpected_input = st.text() | st.none()
fuzz_settings = settings(max_examples=200, derandomize=True, report_multiple_bugs=False)


@fuzz_settings
@given(unexpected_input)
def test_cart_total_no_crash(value):
    result = cart_total(value)
    assert result is None or (type(result) is int and result >= 0)


@fuzz_settings
@given(unexpected_input)
def test_promo_percent_no_crash(value):
    result = promo_percent(value)
    assert result is None or (type(result) is int and 0 <= result <= 100)


@fuzz_settings
@given(unexpected_input)
def test_delivery_zone_no_crash(value):
    assert delivery_zone(value) in (None, "North", "West", "South", "East")


@given(st.lists(st.tuples(st.integers(0, 10_000), st.integers(0, 100)),
                min_size=1, max_size=10))
def test_cart_total_matches_sum(items):
    cart = ",".join(f"item{i}:{price}x{qty}" for i, (price, qty) in enumerate(items))
    assert cart_total(cart) == sum(price * qty for price, qty in items)


@given(st.integers(0, 100), st.sampled_from(("OFF", "off", "Off")))
def test_promo_percent_reads_valid_discount(percent, prefix):
    assert promo_percent(f"{prefix}{percent}") == percent


@given(st.sampled_from(("12", "34", "56", "78")), st.integers(0, 99_999))
def test_delivery_zone_matches_first_digit(digits, suffix):
    expected = {"12": "North", "34": "West", "56": "South", "78": "East"}[digits]
    for digit in digits:
        assert delivery_zone(f"{digit}{suffix:05d}") == expected


def test_cart_total_rejects_malformed_items():
    invalid = (
        "", None, 42, ":10x1", "pen:ax1", "pen:10x", "pen:10xx1",
        "pen:1_0x1", "pen:-10x1", "pen:10x-1", "pen:10x1,",
        "pen:10x1,broken", "pen:10x1:extra", "pen\ncil:10x1",
    )
    for value in invalid:
        assert cart_total(value) is None, repr(value)
    assert cart_total(" pen:10x2, book:250x1 ") == 270

    digit_limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
    if digit_limit:
        digits = "9" * digit_limit
        assert cart_total(f"pen:{digits}x{digits}") is None
        assert cart_total(f"pen:{digits}9x1") is None


def test_promo_percent_rejects_malformed_discounts():
    invalid = ("", None, 42, "SAVE20", "XOFF20", "OFF20OFF", "OFF-1", "OFF101",
               "OFF", "OFF2_0", "OFF٢٠", f"OFF{'9' * 5000}")
    for value in invalid:
        assert promo_percent(value) is None, repr(value)
    assert promo_percent(" off020 ") == 20


def test_delivery_zone_rejects_malformed_pincodes():
    invalid = ("", None, 42, "56008", "5600855", "56A085", "960085", "060085", "５６００８５")
    for value in invalid:
        assert delivery_zone(value) is None, repr(value)
    assert delivery_zone(" 560085 ") == "South"
