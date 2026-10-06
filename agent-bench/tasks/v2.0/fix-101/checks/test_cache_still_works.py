from decorators import memoize


def test_caching_actually_caches():
    calls = {"n": 0}

    @memoize
    def heavy(x):
        calls["n"] += 1
        return x * 2

    assert heavy(9) == 18
    assert heavy(9) == 18
    assert calls["n"] == 1
