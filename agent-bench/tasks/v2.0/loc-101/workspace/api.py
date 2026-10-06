"""接口层（与本缺陷无关，无需改动）。"""
from service import change_email, fetch_profile


def handle_request(action, **kwargs):
    if action == "change_email":
        change_email(kwargs["user_id"], kwargs["email"])
        return {"ok": True}
    return fetch_profile(kwargs["user_id"])
