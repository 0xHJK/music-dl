#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: qq.py
@time: 2019-01-09

QQ音乐搜索和下载

"""

import datetime
import random
import glovar
from core.common import *
from core.exceptions import *
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def qq_search(keyword) -> list:
    ''' 搜索音乐 '''
    count = glovar.get_option('count') or 5
    params = {
        'w': keyword,
        'format': 'json',
        'p': 1,
        'n': count
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://m.y.qq.com',
        'User-Agent': glovar.IOS_USERAGENT
    })
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    music_list = []
    r = s.get('http://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 0:
        raise ResponseError(j)

    for m in j['data']['song']['list']:
        # 获得歌手名字
        singers = []
        for singer in m['singer']:
            singers.append(singer['name'])

        # size = m['size320'] or m['size128']
        size = m['size128']
        music = {
            'title': m['songname'],
            'id': m['songid'],
            'mid': m['songmid'],
            'duration': str(datetime.timedelta(seconds=m['interval'])),
            'singer': '、'.join(singers),
            'album': m['albumname'],
            # 'ext': m['ExtName'],
            'size': round(size / 1048576, 2),
            'source': 'qq'
        }

        music_list.append(music)

    return music_list


def qq_download(music):
    ''' 根据songmid等信息获得下载链接 '''
    # 计算vkey
    guid = str(random.randrange(1000000000, 10000000000))
    params = {
        'guid': guid,
        'format': 'json',
        'json': 3
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://y.qq.com',
        'User-Agent': glovar.IOS_USERAGENT
    })
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    r = s.get('http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 0:
        raise ResponseError(j)

    vkey = j['key']

    for prefix in ['M800', 'M500', 'C400']:
        url = 'http://dl.stream.qqmusic.qq.com/%s%s.mp3?vkey=%s&guid=%s&fromtag=1' % \
              (prefix, music['mid'], vkey, guid)
        size = content_length(url)
        if size > 0:
            music['url'] = url
            music['rate'] = 320 if prefix == 'M800' else 128
            music['size'] = round(size / 1048576, 2)
            break

    music['name'] = '%s - %s.mp3' % (music['singer'], music['title'])

    music_download(music)


search = qq_search
download = qq_download
