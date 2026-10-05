from inventory import remove_out_of_stock


def test_removes_zero_stock():
    assert remove_out_of_stock({"a": 0, "b": 2, "c": 0}) == {"b": 2}
