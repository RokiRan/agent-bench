from fetcher import fetch


def test_timeout_param():
    assert fetch("u") == (200, "<content of u after 3 retries, timeout 10s>")
    assert fetch("u", timeout=5) == (200, "<content of u after 3 retries, timeout 5s>")
    assert fetch("u", 2, 20) == (200, "<content of u after 2 retries, timeout 20s>")
