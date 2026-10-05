from money import round_money


def test_custom_precision():
    assert round_money(3.14159, 3) == 3.142
    assert round_money(1.23456, 4) == 1.2346
    assert round_money(9.999, 2) == 10.0
