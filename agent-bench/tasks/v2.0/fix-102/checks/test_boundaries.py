from report import is_same_week


def test_sunday_same_week():
    assert is_same_week("2026-10-05", "2026-10-11") is True


def test_cross_month_same_week():
    assert is_same_week("2026-08-31", "2026-09-06") is True


def test_different_weeks():
    assert is_same_week("2026-10-11", "2026-10-12") is False


def test_year_boundary():
    assert is_same_week("2025-12-29", "2026-01-04") is True
