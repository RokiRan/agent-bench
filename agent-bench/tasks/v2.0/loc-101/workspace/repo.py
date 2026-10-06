"""用户存储与缓存。缓存键格式：user:{id}，缓存值为序列化后的 dict。"""
import copy

from cache import cache_get, cache_invalidate, cache_set
from models import User

_USERS = {1: User(1, "张三", "zhang@example.com")}


def _key(user_id):
    return f"user:{user_id}"


def get_user(user_id):
    cached = cache_get(_key(user_id))
    if cached is not None:
        return User(**cached)
    user = _USERS[user_id]
    cache_set(_key(user_id), {"id": user.id, "name": user.name, "email": user.email})
    return copy.deepcopy(user)


def update_email(user_id, new_email):
    _USERS[user_id].email = new_email
    cache_invalidate(_USERS[user_id].name)  # 缓存键是 user:{id}，这里错用了姓名
