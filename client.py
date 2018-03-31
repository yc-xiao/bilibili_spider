# -*- coding:utf-8 -*-

from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager
from Downloader import Downloader
import time


class QueueManager(BaseManager):
    pass


if __name__ == '__main__':
    downloader = Downloader('client')
    freeze_support()
    # 注册
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    m = QueueManager(('127.0.0.1', 8003), authkey='helloc'.encode('utf-8'))  # 绑定
    m.connect()  # 连接
    task_queue = m.get_task_queue()  # 获取
    result_queue = m.get_result_queue()  # 获取
    result_queue.put('accept')
    while True:
        try:
            result_queue.put('get')
            user_id = task_queue.get()
            print(user_id)
            if user_id == 'exit':
                result_queue.put('exit')
                break
            data = downloader.parse_user(user_id)
            result_queue.put(data)
        except KeyboardInterrupt:
            print('断开连接')
            result_queue.put('exit')
            break
        except Exception as e:
            print('error_client ', user_id)
            time.sleep(15)
            result_queue.put('error')
            with open('error/test_error.txterror.txt', 'a+') as f:
                f.write('error_client ' + str(user_id) + ' ' + str(e) + '\n')


    '''
    try:
        while True:
            result_queue.put('get')
            user_id = task_queue.get()
            print(user_id)
            if user_id == 'exit':
                result_queue.put('exit')
                break
            data = downloader.parse_user(user_id)
            result_queue.put(data)
    except KeyboardInterrupt:
        print('断开连接')
        result_queue.put('exit')
    except Exception as e:
        with open('error.txt', 'a+') as f:
            f.write('error_client '+str(user_id)+' '+'+str(e)+'\n')
        result_queue.put('exit')
    '''
    '''
    while True:
        result_queue.put('get')
        user_id = task_queue.get()
        print(user_id)
        if user_id == 'exit':
            result_queue.put('exit')
            break
        data = downloader.parse_user(user_id)
        result_queue.put(data)
'''
