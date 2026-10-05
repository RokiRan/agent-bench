from stats import average


def test_empty_returns_zero():
    assert average([]) == 0.0
