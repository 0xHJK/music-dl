#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: kugou.py 
@time: 2019-01-08

酷狗音乐搜索和下载

"""

import datetime
import glovar
from core.common import *
from core.exceptions import *
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def kugou_search(keyword) -> list:
    ''' 搜索音乐 '''
    count = glovar.get_option('count') or 5
    params = {
        'keyword': keyword,
        'platform': 'WebFilter',
        'format': 'json',
        'page': 1,
        'pagesize': count
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({'referer': 'http://www.kugou.com'})
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    music_list = []
    r = s.get('http://songsearch.kugou.com/song_search_v2', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['status'] != 1:
        raise ResponseError(j)

    for m in j['data']['lists']:
        music = {
            'title': m['SongName'],
            'id': m['Scid'],
            'hash': m['FileHash'],
            'duration': str(datetime.timedelta(seconds=m['Duration'])),
            'singer': m['SingerName'],
            'album': m['AlbumName'],
            # 'ext': m['ExtName'],
            'size': round(m['FileSize'] / 1048576, 2),
            'source': 'kugou'
        }
        # 如果有更高品质的音乐选择高品质（尽管好像没什么卵用）
        if m['SQFileHash'] and m['SQFileHash'] != '00000000000000000000000000000000':
            music['hash'] = m['SQFileHash']
        elif m['HQFileHash'] and m['HQFileHash'] != '00000000000000000000000000000000':
            music['hash'] = m['HQFileHash']

        music_list.append(music)

    return music_list


def kugou_download(music):
    ''' 根据hash从酷狗下载音乐 '''
    params = {
        'cmd': 'playInfo',
        'hash': music['hash']
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://m.kugou.com',
        'User-Agent': glovar.IOS_USERAGENT
    })
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    r = s.get('http://m.kugou.com/app/i/getSongInfo.php', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['status'] != 1:
        raise ResponseError(j)

    music['ext'] = j['extName']
    music['name'] = j['fileName'] + '.' + j['extName']
    music['size'] = round(j['fileSize'] / 1048576, 2)
    music['rate'] = j['bitRate']
    music['url'] = j['url']

    music_download(music)


search = kugou_search
download = kugou_download
