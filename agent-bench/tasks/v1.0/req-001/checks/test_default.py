from greet import greet


def test_none_and_blank():
    assert greet(None) == "你好，朋友"
    assert greet("") == "你好，朋友"
    assert greet("   ") == "你好，朋友"
