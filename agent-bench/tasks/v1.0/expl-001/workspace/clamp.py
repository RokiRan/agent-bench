def clamp(value, low, high):
    """将 value 限制在 [low, high] 区间。"""
    if value < high:
        return low
    if value > low:
        return high
    return value
