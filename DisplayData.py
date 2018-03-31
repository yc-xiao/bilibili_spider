# -*- coding:utf-8 -*-
# @Time   ： 2018/3/21 16:30
from SaveData import SaveData
import requests
import os
import time
# SELECT * FROM test ORDER BY fan desc LIMIT 10;
# SELECT * FROM test ORDER BY playmax DESC LIMIT 10;
# SELECT * FROM test ORDER BY playnum DESC LIMIT 10;


class DisplayData(object):
    def __init__(self, name):
        self.name = name
        self.path = r'html/'+name+'.html'
        self.max_fans = 0  # 最大粉丝数前10
        self.max_plays = 0  # 单个播放数前10
        self.total_playnums = 0  # 所有视频播放数前10
        self.savedate = SaveData(name)

    def orderby(self):
        self.savedate.cursor.execute('SELECT * FROM %s ORDER BY fan desc LIMIT 10' % self.name)
        self.max_fans = self.savedate.cursor.fetchall()
        self.savedate.cursor.execute('SELECT * FROM %s ORDER BY playmax DESC LIMIT 10' % self.name)
        self.max_plays = self.savedate.cursor.fetchall()
        self.savedate.cursor.execute('SELECT * FROM %s ORDER BY playnum DESC LIMIT 10' % self.name)
        self.total_playnums = self.savedate.cursor.fetchall()
        self.savedate.close()

    def display(self):
        self.orderby()
        self.name = self.name + '.html'
        if not self.max_plays:
            return 1
        temp = [self.max_fans, self.max_plays, self.total_playnums]
        user_id, name, fans, play_num, total_play_nums, detail, img_url, user_url = 0, 1, 2, 3, 4, 5, 6, 7
        user = dict()
        for i in range(3):
            for j in range(10):
                user[temp[i][j][user_id]] = temp[i][j][img_url]
        for k, v in user.items():
            path = r'img/'+str(k)+'.jpg'
            if not os.path.exists(path):
                res = requests.get(v)
                time.sleep(0.5)
                content = res.content
                if content:
                    with open(path, 'wb') as f:
                        f.write(content)
        start = '''<html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>Document</title>
                        <link rel="stylesheet" type="text/css" href="mode.css">
                    </head>
                    <body><div class="main">
                '''
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(start)
            for i in range(3):
                f.write('<div class="box"><ol>')
                num = i + 2
                for j in range(10):
                    f.write('<li>%s.<a href="%s">%s</a><span class="right">%s</span></li>' % (j+1, temp[i][j][user_url], temp[i][j][name], temp[i][j][num]))
                    f.write('<div class="hidden_box"><img src="../img/%s.jpg" alt="">' % (temp[i][j][user_id]))
                    f.write('<span class="detail">%s</span></div>' % temp[i][j][detail])
                f.write('</ol></div>')
            f.write('</body></html>')