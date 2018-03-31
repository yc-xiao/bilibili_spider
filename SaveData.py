# -*- coding:utf-8 -*-
# @Time   ： 2018/3/21 16:30
import pymysql
import pickle
import os


class SaveData(object):
    def __init__(self, name):
        self.datas = []
        self.name = name
        self.error_path = r'error/' + name + '_error.txt'
        set_mysql = {'host': '127.0.0.1', 'user': 'root', 'password': '333333', 'database': 'mydb', 'charset': 'utf8'}
        self.conn = pymysql.connect(**set_mysql)
        self.cursor = self.conn.cursor()
        self.cursor.execute('show tables')
        table_tuple = self.cursor.fetchall()
        # user_id, name, playnum, fan, playmax
        if (name,) not in table_tuple:
            create = 'create table if not exists %s(id int unsigned primary key,name tinytext,' \
                     'fan int unsigned,playmax int unsigned,playnum int unsigned,' \
                     'sign tinytext,img tinytext,user_url tinytext)' % (name)
            self.cursor.execute(create)

    # 将用户集合保存到pickle文件
    def save_user_pickle(self, path, user_ids):
        path = r'pickle/'+path
        if user_ids:
            with open(path, 'wb') as f:
                pickle.dump(user_ids, f)
                print('保存成功!')

    # 获取用户集合
    def get_user_pickle(self, path):
        path = r'pickle/' + path
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)

    # 获取已搜索用户集合
    def get_used_user_pickle(self, path):
        return self.get_user_pickle(path)

    # 保存数据
    def save_data(self, datas):
        self.datas.append(datas)
        self.save_mysql()
        if len(self.datas) == 100:
            self.save_mysql()

    def save_mysql(self):
        for data in self.datas:
            insert = 'insert %s values(%s,"%s",%s,%s,%s,"%s","%s","%s")' % (
                self.name, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
            try:
                self.cursor.execute(insert)
            except Exception as e:
                with open(self.error_path, 'a+') as f:
                    f.write(str(data[0]))
                    f.write('60'+str(e)+'\n')
        self.conn.commit()
        self.datas.clear()

    def close(self):
        self.save_mysql()
        self.cursor.close()
        self.conn.close()

