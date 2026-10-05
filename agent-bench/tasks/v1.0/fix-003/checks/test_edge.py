from inventory import remove_out_of_stock


def test_empty_dict():
    assert remove_out_of_stock({}) == {}


def test_nothing_to_remove():
    assert remove_out_of_stock({"x": 1}) == {"x": 1}
