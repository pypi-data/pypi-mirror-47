import os
import re
import copy
import json
import requests
from urllib import parse

import BiliUtil.static_value as v
import BiliUtil.static_func as f
from BiliUtil.bili_album import Album


class Channel:
    cookie = None

    uid = None
    cid = None

    name = None
    cover = None
    count = None
    album_list = list()

    def __init__(self, uid=None, cid=None):
        self.set_channel(uid, cid)

    def set_channel(self, uid, cid):
        self.uid = uid
        self.cid = cid
        self.name = None
        self.cover = None
        self.count = None
        self.album_list = list()

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        uid = re.match('/([0-9]+)/channel/detail', input_url.path).group(1)
        cid = parse.parse_qs(input_url.query)['cid'][0]
        self.set_channel(uid, cid)

    def set_cookie(self, cookie):
        self.cookie = cookie
        for album in self.album_list:
            album.set_cookie(cookie)

    def get_channel_info(self):
        if self.uid is None or self.cid is None:
            raise BaseException('缺少必要的参数')

        param = {
            'mid': str(self.uid),
            'cid': str(self.cid),
            'pn': 1,  # 当前页码下标
            'ps': 30,  # 每页视频数量
            'order': 0  # 默认排序
        }
        while True:
            f.print_1('正在获取视频列表-{}...'.format(param['pn']), end='')
            http_result = requests.get(v.URL_UP_CHANNEL, params=param,
                                       headers=f.new_http_header(v.URL_UP_CHANNEL))
            if http_result.status_code == 200:
                f.print_g('OK {}'.format(http_result.status_code))
            else:
                f.print_r('RE {}'.format(http_result.status_code))
            json_data = json.loads(http_result.text)
            if json_data['code'] != 0:
                raise BaseException('获取数据的过程发生错误')

            self.name = json_data['data']['list']['name']
            self.cover = json_data['data']['list']['cover']
            self.count = str(json_data['data']['list']['count'])

            for album in json_data['data']['list']['archives']:
                av = Album(album['aid'])
                av.set_cookie(self.cookie)
                self.album_list.append(av)

            # 循环翻页获取并自动退出循环
            if len(self.album_list) >= int(json_data['data']['page']['count']):
                break
            else:
                param['pn'] += 1
        return copy.deepcopy(vars(self))

    def get_channel_data(self, base_path='', name_path=False, max_length=None, exclude_list=None):
        if len(self.album_list) == 0:
            self.get_channel_info()

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            if len(temp_name) == 0:
                temp_name = self.cid
            cache_path = base_path + '/{}'.format(temp_name)
        else:
            cache_path = base_path + '/{}'.format(self.cid)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        f.print_1('正在获取频道封面--', end='')
        f.print_b('channel:{}'.format(self.name))
        http_result = requests.get(self.cover)
        with open(cache_path + '/cover.jpg', 'wb') as file:
            file.write(http_result.content)
        f.print_g('[OK]', end='')
        f.print_1('视频封面已保存')

        for album in self.album_list:
            if exclude_list is not None and album.aid in exclude_list:
                continue
            album.get_album_data(cache_path, name_path, max_length)

        with open(cache_path + '/info.json', 'w', encoding='utf8') as file:
            file.write(str(json.dumps(self.get_dict_info())))

    def get_exist_list(self, base_path='', name_path=False):
        if len(self.album_list) == 0:
            self.get_channel_info()

        base_path = os.path.abspath(base_path)  # 获取绝对路径地址
        if name_path:
            # 检查路径名中的特殊字符
            temp_name = re.sub(r"[\/\\\:\*\?\"\<\>\|\s'‘’]", '_', self.name)
            if len(temp_name) == 0:
                temp_name = self.cid
            cache_path = base_path + '/{}'.format(temp_name)
        else:
            cache_path = base_path + '/{}'.format(self.cid)
        if not os.path.exists(cache_path):
            return []

        exist_list = []
        for album in self.album_list:
            if album.is_exist(cache_path, name_path):
                exist_list.append(album.aid)

        return exist_list

    def get_av_list(self):
        if len(self.album_list) == 0:
            self.get_channel_info()

        av_list = []
        for album in self.album_list:
            av_list.append(album.aid)

        return av_list

    def get_dict_info(self):
        json_data = copy.deepcopy(vars(self))

        album_list = []
        for album in self.album_list:
            album_list.append(album.get_dict_info())
        json_data['album_list'] = album_list
        return json_data
