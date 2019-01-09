#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: qq.py
@time: 2019-01-09

QQ音乐搜索和下载

"""

import datetime
import glovar
from core.common import *
from core.exceptions import *
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def qq_search(keyword, count=5) -> list:
    ''' 搜索音乐 '''
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

        size = m['size320'] or m['size128']
        music = {
            'title': m['songname'],
            'id': m['songid'],
            'mid': m['songmid'],
            'length': str(datetime.timedelta(seconds=m['interval'])),
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
    params = {
        'guid': '5150825362',
        'format': 'json',
        'json': 3
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://y.qq.com',
        'User-Agent': glovar.IOS_USERAGENT
    })

    r = s.get('http://base.music.qq.com/fcgi-bin/fcg_musicexpress.fcg', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 0:
        raise ResponseError(j)

    vkey = j['key']

    for prefix in ['M800', 'M500', 'C400']:
        url = 'http://dl.stream.qqmusic.qq.com/%s%s.mp3?vkey=%s&guid=5150825362&fromtag=1' % \
              (prefix, music['mid'], vkey)
        if url_available(url):
            music['url'] = url
            music['rate'] = 320 if prefix == 'M800' else 128
            break

    music['name'] = '%s - %s.mp3' % (music['singer'], music['title'])

    music_download(music)


search = qq_search
download = qq_download
