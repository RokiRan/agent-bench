from service import change_email, fetch_profile


def test_email_fresh_after_update():
    fetch_profile(1)  # 建立缓存
    change_email(1, "new@example.com")
    assert fetch_profile(1)["email"] == "new@example.com"
