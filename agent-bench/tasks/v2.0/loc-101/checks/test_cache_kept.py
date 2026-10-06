import cache
from repo import get_user


def test_cache_still_populated():
    cache.cache_invalidate("user:1")
    get_user(1)
    assert cache.cache_get("user:1") is not None
