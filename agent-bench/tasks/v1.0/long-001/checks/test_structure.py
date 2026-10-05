import os


def test_renamed():
    assert os.path.exists("helpers.py")
    assert not os.path.exists("utils.py")
