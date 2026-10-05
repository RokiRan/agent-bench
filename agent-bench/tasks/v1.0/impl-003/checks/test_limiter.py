from ratelimit import RateLimiter


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


def test_allows_up_to_limit():
    clock = FakeClock()
    rl = RateLimiter(2, 10, now=clock)
    assert rl.allow() is True
    assert rl.allow() is True


def test_blocks_over_limit():
    clock = FakeClock()
    rl = RateLimiter(2, 10, now=clock)
    rl.allow()
    rl.allow()
    assert rl.allow() is False


def test_window_resets():
    clock = FakeClock()
    rl = RateLimiter(1, 10, now=clock)
    assert rl.allow() is True
    assert rl.allow() is False
    clock.t += 11
    assert rl.allow() is True
