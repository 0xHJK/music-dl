#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
"""
@author: HJK 
@file: flac.py 
@time: 2019-01-25

从百度音乐获得flac无损音乐

"""

import datetime
import glovar
from core.common import *
from core.exceptions import *
from utils.customlog import CustomLog

logger = CustomLog(__name__).getLogger()

def flac_search(keyword) -> list:
    ''' 搜索无损音乐 '''
    params = {
        'word': keyword,
        'version': '2',
        'from': 0,
    }

    music_list = []
    r = requests.get('http://sug.music.baidu.com/info/suggestion', params=params,
                     proxies=glovar.get_option('proxies'))
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    for m in j['data']['song']:
        music = {
            'title': m['songname'],
            'id': m['songid'],
            'singer': m['artistname'],
            'source': 'flac'
        }
        m_params = {'songIds': music['id'], 'type': 'flac'}
        # 不在同一个session能提高请求成功率
        mr = requests.get('http://music.baidu.com/data/music/fmlink', params=m_params,
                          proxies=glovar.get_option('proxies'))
        if mr.status_code != requests.codes.ok:
            raise RequestError(mr.text)
        mj = mr.json()
        if mj['errorCode'] != 22000:
            continue
        if not mj['data']['songList']:
            continue
        mj_music = mj['data']['songList'][0]
        music['duration'] = str(datetime.timedelta(seconds=mj_music['time']))
        size = mj_music['size'] or 0
        music['size'] = round(size / 1048576, 2)
        music['rate'] = mj_music['rate']
        music['ext'] = mj_music['format']
        music['url'] = mj_music['songLink']
        music['album'] = mj_music['albumName']
        music['name'] = '%s - %s.%s' % (mj_music['artistName'], mj_music['songName'], mj_music['format'])

        music_list.append(music)

    return music_list


def flac_download(music):
    ''' 从百度音乐下载无损音乐 '''
    music_download(music)

search = flac_search
download = flac_download
