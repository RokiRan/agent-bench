"""数据模型。"""
import json


class Product:
    def __init__(self, sku, title, price):
        self.sku = sku
        self.title = title
        self.price = price

    def to_dict(self):
        return {"sku": self.sku, "title": self.title, "price": self.price}
