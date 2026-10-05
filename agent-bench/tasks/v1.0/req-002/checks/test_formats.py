from dateutil import parse_date


def test_dash_format():
    assert parse_date("2026-10-05") == (2026, 10, 5)


def test_slash_format():
    assert parse_date("2026/10/5") == (2026, 10, 5)
