# -*- coding:utf-8 -*-


import requests
import json
import time


class Downloader(object):

    def __init__(self, name):
        self.header = dict()
        self.error_path = r'error/' + name + '_error.txt'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'
        self.header['User-Agent'] = self.user_agent

    # 访问网页下载
    def download(self, url):
        try:
            response = requests.get(url, headers=self.header, timeout=5)
            time.sleep(0.5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            with open(self.error_path, 'a+') as f:
                f.write('26network_error'+str(e)+url+'\n')

    # 首页解析，搜索100名用户id
    def parse(self, data):
        user_ids = []
        datas = json.loads(data)
        datas = datas['rank']['list']
        for user in datas:
            user_ids.append(user['aid'])
        return user_ids

    # 解析用户，搜索用户粉丝
    def parse_following(self, user_id):
        url = 'https://api.bilibili.com/x/relation/stat?vmid=%s' % user_id
        text = self.download(url)
        if text:
            text = json.loads(text)
            following = text['data']['following']
        if following:
            user_ids = []
            if following < 50:
                url = 'https://api.bilibili.com/x/relation/followings?vmid=%s&ps=50' % user_id
                text = self.download(url)
                text = json.loads(text)
                text = text['data']['list']
                for data in text:
                    user_ids.append(data['mid'])
                return user_ids
            else:
                page = int(following)//20 + 1
                if page > 5:
                    page = 5
                urls = ['https://api.bilibili.com/x/relation/followings?vmid={}&ps=20&pn={}'.format(user_id,n)
                        for n in range(1, page+1)]
                for url in urls:
                    text = self.download(url)
                    text = json.loads(text)
                    text = text['data']['list']
                    for data in text:
                        user_ids.append(data['mid'])
                return user_ids

    # 解析用户，搜索用户具体信息
    def parse_user(self, user_id):
        # user_name  user_url  user_img  user_fans user_video_playnum user_works
        fan_url = 'https://api.bilibili.com/x/relation/stat?vmid=%s&jsonp=jsonp' % user_id
        play_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&pagesize=50&order=click' % user_id
        url = 'https://space.bilibili.com/ajax/member/GetInfo'
        user_url = 'https://space.bilibili.com/%s#/' % user_id
        fan_data = self.download(fan_url)
        fan = json.loads(fan_data)['data']['follower']
        name, img, playnum, sign = self.name_img_parse(url, user_id)
        playmax = self.parse_play(play_url)
        return user_id, name, fan, playmax, playnum, sign, img, user_url
        # return user_id, name, playnum, fan, playmax

    # 解析用户字段
    def name_img_parse(self, url, user_id):
        user_url = 'https://space.bilibili.com/%s' % user_id
        header = {'User-Agent': self.user_agent, 'Referer': url}
        data = {'mid': user_id, 'csrf': 'null'}
        try:
            response = requests.post(url, headers=header, data=data, timeout=5)
            time.sleep(0.5)
            if response.status_code == 200:
                user_datas = json.loads(response.text)
                name = user_datas['data']['name']
                img = user_datas['data']['face']
                playnum = user_datas['data']['playNum']
                sign = user_datas['data']['sign']
                return name, img, playnum, sign
        except Exception as e:
            with open(self.error_path, 'a+') as f:
                f.write('99network_error'+str(e)+url+'\n')

    # 解析用户字段
    def parse_play(self, url):
        playmax = 0
        other = self.download(url)
        count = json.loads(other)['data']['count']
        vlist = json.loads(other)['data']['vlist']
        if count:
            playmax = vlist[0]['play']
        return playmax





