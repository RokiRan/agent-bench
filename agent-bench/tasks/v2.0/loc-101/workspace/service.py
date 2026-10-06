"""对外服务接口。"""
from repo import get_user, update_email


def change_email(user_id, new_email):
    update_email(user_id, new_email)


def fetch_profile(user_id):
    user = get_user(user_id)
    return {"id": user.id, "name": user.name, "email": user.email}
