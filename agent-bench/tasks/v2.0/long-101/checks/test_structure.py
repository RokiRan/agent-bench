import json

from serializers import product_to_json
from store import describe, find_by_sku


def test_json_uses_name_key():
    payload = json.loads(product_to_json(find_by_sku("A001")))
    assert payload["name"] == "马克杯"
    assert "title" not in payload


def test_describe_uses_name():
    assert describe("A001") == "马克杯（A001）"
