"""周报工具。"""


def is_same_week(date_a, date_b):
    """判断两个日期（YYYY-MM-DD）是否在同一自然周（周一为一周开始）。"""
    y1, m1, d1 = (int(x) for x in date_a.split("-"))
    y2, m2, d2 = (int(x) for x in date_b.split("-"))
    return (y1, m1, d1 // 7) == (y2, m2, d2 // 7)
