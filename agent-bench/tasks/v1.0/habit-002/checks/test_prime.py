from prime import is_prime


def test_primes():
    assert all(is_prime(n) for n in [2, 3, 5, 7, 13])


def test_non_primes():
    assert not any(is_prime(n) for n in [0, 1, 4, 9, 100])
