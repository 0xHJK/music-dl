#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
"""
@author: HJK 
@file: baidu.py 
@time: 2019-01-20

百度音乐搜索和下载

"""

import datetime
import glovar
from core.common import *
from core.exceptions import *
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def baidu_search(keyword) -> list:
    ''' 搜索音乐 '''
    count = glovar.get_option('count') or 5
    params = {
        'query': keyword,
        'method': 'baidu.ting.search.common',
        'format': 'json',
        'page_no': 1,
        'page_size': count
    }
    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({'referer': 'http://music.baidu.com/'})
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    music_list = []
    r = s.get('http://musicapi.qianqian.com/v1/restserver/ting', params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    for m in j['song_list']:
        music = {
            'title': m['title'].replace('<em>', '').replace('</em>', ''),
            'id': m['song_id'],
            'singer': m['author'].replace('<em>', '').replace('</em>', ''),
            'album': m['album_title'].replace('<em>', '').replace('</em>', ''),
            'source': 'baidu'
        }
        s.headers.update({'referer': 'http://music.baidu.com/song/' + m['song_id']})
        m_params = {'songIds': m['song_id']}
        mr = s.get('http://music.baidu.com/data/music/links', params=m_params)
        if mr.status_code != requests.codes.ok:
            raise RequestError(mr.text)
        mj = mr.json()
        if not mj['data']['songList']:
            continue
        mj_music = mj['data']['songList'][0]
        music['duration'] = str(datetime.timedelta(seconds=mj_music['time']))
        size = mj_music['size'] or 0
        music['size'] = round(size / 1048576, 2)
        music['rate'] = mj_music['rate']
        music['ext'] = mj_music['format']
        music['url'] = mj_music['songLink']
        music['name'] = '%s - %s.%s' % (mj_music['artistName'], mj_music['songName'], mj_music['format'])

        music_list.append(music)

    return music_list


def baidu_download(music):
    ''' 从百度音乐下载音乐 '''
    music_download(music)

search = baidu_search
download = baidu_download
