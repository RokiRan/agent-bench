from paginate import paginate


def test_middle_page():
    assert paginate(list(range(10)), 2, 3) == [3, 4, 5]


def test_last_partial_page():
    assert paginate(list(range(10)), 4, 3) == [9]
