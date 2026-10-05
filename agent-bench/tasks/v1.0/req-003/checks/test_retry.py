from retry import retry


def test_succeeds_after_failures():
    calls = {"n": 0}

    @retry(times=3)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_gives_up_after_times():
    calls = {"n": 0}

    @retry(times=2)
    def always_fail():
        calls["n"] += 1
        raise ValueError("x")

    try:
        always_fail()
    except ValueError:
        pass
    else:
        raise AssertionError("应在重试耗尽后抛出最后一次异常")
    assert calls["n"] == 2


def test_no_retry_on_success():
    calls = {"n": 0}

    @retry(times=5)
    def fine():
        calls["n"] += 1
        return 1

    assert fine() == 1
    assert calls["n"] == 1
