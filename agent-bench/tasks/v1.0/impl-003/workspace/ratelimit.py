class RateLimiter:
    """固定窗口限流器：window 秒内最多允许 limit 次。"""

    def __init__(self, limit, window, now=None):
        raise NotImplementedError

    def allow(self):
        """本次调用是否放行。"""
        raise NotImplementedError
