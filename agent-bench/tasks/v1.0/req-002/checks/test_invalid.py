import pytest

from dateutil import parse_date


@pytest.mark.parametrize("bad", ["2026年10月5日", "2026-13-01", "2026-02-30", "abc", "2026-10"])
def test_invalid_raises(bad):
    with pytest.raises(ValueError):
        parse_date(bad)
