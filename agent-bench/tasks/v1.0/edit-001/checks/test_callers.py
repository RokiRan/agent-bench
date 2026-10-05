from report import summarize


def test_summarize_unchanged():
    assert summarize([1.1, 2.2]) == "共 2 笔，合计 3.3"
