def paginate(items, page, per_page):
    """返回第 page 页（从 1 开始计数）的元素列表。"""
    start = page * per_page
    end = start + per_page
    return items[start:end]
