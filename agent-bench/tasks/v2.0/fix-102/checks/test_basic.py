from report import is_same_week


def test_same_day():
    assert is_same_week("2026-10-07", "2026-10-07") is True


def test_far_apart():
    assert is_same_week("2026-01-05", "2026-03-09") is False
