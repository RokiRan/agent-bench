"""购物车结算。"""
from pricing import apply_discount


def checkout_total(items, discount):
    """返回折扣后总价。items 为 (名称, 单价) 列表，discount 如 0.1。"""
    total = sum(price for _, price in items)
    discounted = apply_discount(total, discount)
    return apply_discount(discounted, discount)
