from notify import ping
from pipeline import run
from report import fetch_text


def test_positional_callers_intact():
    assert "<content of u after 1 retries, timeout 10s>" in run("u")
    assert ping("u") is True
    assert fetch_text("u").endswith("timeout 10s>")
