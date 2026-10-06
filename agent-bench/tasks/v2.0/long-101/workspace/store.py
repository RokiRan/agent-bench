"""商品仓库。"""
from models import Product

PRODUCTS = [Product("A001", "马克杯", 49.9)]


def find_by_sku(sku):
    for p in PRODUCTS:
        if p.sku == sku:
            return p
    return None


def describe(sku):
    p = find_by_sku(sku)
    return f"{p.title}（{p.sku}）" if p else None
