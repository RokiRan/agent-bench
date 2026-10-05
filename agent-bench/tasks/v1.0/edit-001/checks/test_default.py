from money import round_money


def test_default_precision_kept():
    assert round_money(3.14159) == 3.14
