from user import User


def test_old_method_removed():
    assert not hasattr(User, "get_name")


def test_new_method_exists():
    assert hasattr(User, "display_name")
