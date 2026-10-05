class LRUCache:
    """容量有限的 LRU 缓存。"""

    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        """命中返回值并标记为最近使用；未命中返回 None。"""
        raise NotImplementedError

    def put(self, key, value):
        """写入；超出容量时淘汰最久未使用的项。"""
        raise NotImplementedError
