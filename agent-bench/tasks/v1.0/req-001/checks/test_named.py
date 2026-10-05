from greet import greet


def test_named():
    assert greet("小明") == "你好，小明"
    assert greet("  小红  ") == "你好，小红"
