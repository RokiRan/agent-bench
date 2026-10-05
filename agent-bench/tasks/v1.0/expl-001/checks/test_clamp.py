from clamp import clamp


def test_inside_range():
    assert clamp(5, 1, 10) == 5


def test_bounds():
    assert clamp(-5, 1, 10) == 1
    assert clamp(99, 1, 10) == 10


def test_edges():
    assert clamp(1, 1, 10) == 1
    assert clamp(10, 1, 10) == 10
