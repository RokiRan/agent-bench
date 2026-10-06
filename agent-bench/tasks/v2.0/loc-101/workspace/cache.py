"""简单内存缓存。"""

_STORE = {}


def cache_get(key):
    return _STORE.get(key)


def cache_set(key, value):
    _STORE[key] = value


def cache_invalidate(key):
    _STORE.pop(key, None)
