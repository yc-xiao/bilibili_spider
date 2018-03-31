# -*- coding:utf-8 -*-
# @Time   ： 2018/3/21 10:10
from Downloader import Downloader
from URLManger import UrlManger
from SaveData import SaveData
from DisplayData import DisplayData
import time
import os


class Spider(object):

    def __init__(self, name, used_path):
        self.name = name
        self.used_path = used_path
        self.error_path = r'error/'+ name + '_error.txt'
        self.downloader = Downloader(name)
        self.urlmanager = UrlManger()
        self.savedata = SaveData(name)
        self.displaydata = DisplayData(name)

    # 搜索排行榜及其一二级关注者，放入待搜索集合内
    def crawl(self, url, path):
        data = self.downloader.download(url)
        user_ids = set(self.downloader.parse(data))
        self.urlmanager.add_user(user_ids)
        self.get_following_users(user_ids, 1)
        first_follow_user_ids = self.urlmanager.get_user() - user_ids
        self.get_following_users(first_follow_user_ids, 2)
        self.savedata.save_user_pickle(path, self.urlmanager.get_user())
        print('用户搜索完成，总有%d用户' % self.urlmanager.get_user_size())

    # 搜索失败的用户重新搜索
    def crawl_error_user(self):
        name = r'error/'+self.name + '_error_user.txt'
        if os.path.exists(name):
            with open(name, 'r') as f:
                user_ids = f.readlines()
            user_ids = [int(x) for x in user_ids]
            print('再次搜索用户共%d人' % len(user_ids))
            self.urlmanager.add_user(user_ids)
            self.crawl_data()

    # 搜索用户关注者
    def get_following_users(self, user_ids, n):
        num, temp = 0, 0
        total = len(user_ids)
        average = total // 10 - 1
        print('已收录用户数%d' % (self.urlmanager.get_user_size()))
        print('待搜索%d级用户数%d' % (n, total))

        # 多进程
        for user_id in user_ids:
            num += 1
            if num > average:
                temp += 10
                print('搜索%d级用户的进度为%d' % (n, temp) + '%')
                num = 0
            try:
                following_user_ids = self.downloader.parse_following(user_id)
                self.urlmanager.add_user(following_user_ids)
            except Exception as e:
                with open(self.error_path, 'a+') as f:
                    f.write('63'+str(e)+'\n')
                    f.write('搜索失败的用户id号:', user_id)
        print('搜索%d级用户完成' % n)

    # 程序起始，加载数据
    def load_users(self, path, used_path):
        self.used_path = used_path
        users = self.savedata.get_user_pickle(path)
        used_users = self.savedata.get_used_user_pickle(used_path)
        if not used_users:
            used_users = set()
        users = users - used_users
        print(len(users))
        print(len(used_users))
        self.urlmanager.add_user(users)
        self.urlmanager.add_used__user(used_users)
        self.user_total = self.urlmanager.get_user_size()
        print('加载完成还需要搜索用户%d人' % self.user_total)

    # 搜索用户的有关信息(粉丝数以视频播放数)
    def crawl_data(self):
        while True:
            user_id = self.urlmanager.get_user_id()
            if user_id:
                try:
                    data = self.downloader.parse_user(user_id)
                    self.savedata.save_data(data)
                    print(user_id)
                except KeyboardInterrupt:
                    print('停止')
                    break
                except Exception as e:
                    with open(self.error_path, 'a+') as f:
                        f.write('168error_crawl_data ' + str(e) + '\n')
            else:
                self.savedata.save_user_pickle(self.used_path, self.urlmanager.get_used_user())
                self.savedata.close()
                print('172')
                break

    # 程序异常中断
    def save(self):
        self.savedata.save_user_pickle(self.used_path, self.urlmanager.get_used_user())
        self.savedata.close()
        print('107')









