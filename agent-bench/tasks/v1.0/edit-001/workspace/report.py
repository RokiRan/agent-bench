from money import round_money


def summarize(amounts):
    """返回汇总字符串，如 '共 3 笔，合计 12.35'。"""
    total = round_money(sum(amounts))
    return f"共 {len(amounts)} 笔，合计 {total}"
