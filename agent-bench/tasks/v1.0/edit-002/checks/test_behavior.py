from hello import hello
from user import User


def test_hello_behavior():
    assert hello(User("小明")) == "你好，小明"


def test_display_name_works():
    assert User("x").display_name() == "x"
