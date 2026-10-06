"""业务服务：运费与配送时效查询。"""
from decorators import memoize


@memoize
def shipping_fee(region):
    fees = {"华东": 5, "华北": 8}
    return fees.get(region, 15)


@memoize
def delivery_days(region):
    days = {"华东": 1, "华北": 2}
    return days.get(region, 5)
