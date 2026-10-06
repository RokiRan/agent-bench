import pytest

from models import Product


def test_negative_price():
    with pytest.raises(ValueError, match="价格非法"):
        Product("X", "y", -0.01)


def test_zero_price_ok():
    assert Product("X", "y", 0).price == 0
