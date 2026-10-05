from greet_dup import hello_cn, hello_en, hello_jp


def test_outputs_unchanged():
    assert hello_cn("小明") == "你好，小明！"
    assert hello_en("Tom") == "Hello, Tom!"
    assert hello_jp("健太") == "こんにちは、健太！"
