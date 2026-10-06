"""数据模型。"""


class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email
