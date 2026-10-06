from store import find_by_sku


def test_find():
    assert find_by_sku("A001").title == "马克杯"
