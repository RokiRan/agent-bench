from fib import fib


def test_base():
    assert fib(0) == 0
    assert fib(1) == 1


def test_sequence():
    assert fib(5) == 5
    assert fib(10) == 55
