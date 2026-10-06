"""通用装饰器工具。"""

_CACHE = {}


def memoize(func):
    """缓存函数结果：相同参数直接返回缓存。"""

    def wrapper(*args):
        key = args
        if key not in _CACHE:
            _CACHE[key] = func(*args)
        return _CACHE[key]

    return wrapper
