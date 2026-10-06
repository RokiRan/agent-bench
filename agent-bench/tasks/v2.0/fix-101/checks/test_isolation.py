from service import delivery_days, shipping_fee


def test_no_cross_contamination():
    assert shipping_fee("华东") == 5
    assert delivery_days("华东") == 1


def test_reverse_order():
    assert delivery_days("华北") == 2
    assert shipping_fee("华北") == 8
