from stats import average


def test_normal_cases():
    assert average([1, 2, 3]) == 2
    assert abs(average([0.5, 1.5]) - 1.0) < 1e-9
