from topk import topk_frequent


def test_basic():
    assert topk_frequent("aabbbcc", 2) == [("b", 3), ("a", 2)]


def test_tie_break_ascending():
    assert topk_frequent("aabb", 2) == [("a", 2), ("b", 2)]


def test_k_exceeds_unique():
    assert topk_frequent("ab", 5) == [("a", 1), ("b", 1)]
