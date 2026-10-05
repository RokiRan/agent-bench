from cart import checkout_total


def test_single_item():
    assert checkout_total([("书", 100)], 0.1) == 90.0


def test_multi_items():
    assert checkout_total([("a", 100), ("b", 50)], 0.1) == 135.0


def test_zero_discount():
    assert checkout_total([("a", 100), ("b", 50)], 0) == 150.0
