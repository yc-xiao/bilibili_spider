# -*- coding:utf-8 -*-
# @Time   ： 2018/3/29 18:58
from Spider import Spider
from multiprocessing.managers import BaseManager
from multiprocessing import Queue, Process, Pool
import time
import os


class QueneManager(BaseManager):
    pass

task_queue = Queue()
result_queue = Queue()


def get_task():
    return task_queue


def get_result():
    return result_queue


def server(spider_main):
    print('启动服务器')
    # 注册函数
    QueneManager.register('get_task_queue', callable=get_task)
    QueneManager.register('get_result_queue', callable=get_result)
    # 绑定端口
    manage = QueneManager(address=('127.0.0.1', 8003), authkey='helloc'.encode('utf-8'))
    # 启动监听
    manage.start()
    # 获取队列
    task = manage.get_task_queue()
    result = manage.get_result_queue()
    print('我是服务器,正在等待连接。')
    client_num, temp, num = 0, 0, 0  # num用于记录用户连接数
    total = spider_main.urlmanager.get_user_size()
    average = total // 10 - 1  # 平均数用于显示进度
    while True:
        try:
            data = result.get(timeout=30)
            if data == 'get':
                user_id = spider_main.urlmanager.get_user_id()
                num += 1
                print(user_id)
                if not user_id:
                    task.put('exit')
                    break
                elif num == average:
                    temp += 10
                    num = 0
                    print('搜索进度为%d' % temp + '%')
                task.put(user_id)
            elif data == 'exit':
                client_num -= 1
                print('当前连接数为%d' % client_num)
                if not client_num:
                    break
            elif data == 'accept':
                client_num += 1
                print('当前连接数为%d' % client_num)
            elif data == 'error':
                name = r'error/' + spider_main.name + '_error_user.txt'
                with open(name, 'a+') as f:
                    f.write(str(user_id)+'\n')
            else:
                spider_main.savedata.save_data(data)
        except Exception as e:
            with open('error/error.txt', 'a+') as f:
                f.write('error/error_server 76')
                f.write(str(e)+'\n')
            print('1010')
            break
    manage.shutdown()
    spider_main.save()

if __name__ == "__main__":

    pickle = os.listdir('pickle/')
    print('当前的已保存搜索文件:', pickle)
    name = input('输入搜索代号:')
    path = name + '.pickle'
    used_path = name + '_used.pickle'
    spider_main = Spider(name, used_path)
    if path not in pickle:
        start = time.time()
        url = 'https://www.bilibili.com/index/rank/all-30-3.json'
        spider_main.crawl(url, path)
        
        try:
            spider_main.crawl(url, path)
        except Exception as e:
            with open('error/error.txt', 'a+') as f:
                f.write('94'+str(e) + '\n')
                
        end = time.time()
        times = int(end - start)
        if times > 60:
            mins = times//60
            second = times - mins * 60
            print('搜索用户所用时间为%d分%d秒' % (mins, second))
        else:
            print('搜索用户所用时间为%d秒' % times)
    else:
        # 加载先前下载好的文件
        spider_main.load_users(path, used_path)
    # 启动服务
    server(spider_main)
    print('关闭服务,显示数据')
    # 搜索用户结束，则重新搜索之前搜索失败的用户集合
    if not spider_main.urlmanager.get_user_size():
        spider_main.crawl_error_user()

    if not spider_main.displaydata.display():
        os.chdir('html')
        os.system(name + '.html')
    print('程序结束')
