# -*- coding:utf-8 -*-


class UrlManger(object):
    def __init__(self):
        self.user_ids = set()
        self.used_user_ids = set()

    # 添加用户
    def add_user(self, user_ids):
        if user_ids:
            for user_id in user_ids:
                self.user_ids.add(user_id)

    # 添加已搜索用户
    def add_used__user(self, user_ids):
        if user_ids:
            for user_id in user_ids:
                self.used_user_ids.add(user_id)

    # 获取用户的集合
    def get_user(self):
        return self.user_ids

    # 获取已搜索用户的集合
    def get_used_user(self):
        return self.used_user_ids

    # 获取待搜索用户
    def get_user_id(self):
        try:
            user_id = self.user_ids.pop()
        except:
            return None
        self.used_user_ids.add(user_id)
        return user_id

    # 获取用户集合的大小
    def get_user_size(self):
        return len(self.user_ids)

