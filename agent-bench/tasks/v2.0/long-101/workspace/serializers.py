"""序列化输出。"""
import json


def product_to_json(product):
    return json.dumps(product.to_dict(), ensure_ascii=False, sort_keys=True)
