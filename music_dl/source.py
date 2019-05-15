#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: source.py
@time: 2019-05-13
"""

"""
    Music source proxy object
"""

import threading
import importlib
import traceback
import click
from . import config
from .utils import colorize
from .exceptions import *

class MusicSource:
    """
        Music source proxy object
    """
    def __init__(self):
        pass

    def search(self, keyword, sources_list) -> list:
        sources_map = {
            "baidu": "baidu",
            "flac": "flac",
            "kugou": "kugou",
            "netease": "netease",
            "163": "netease",
            "qq": "qq",
            "xiami": "xiami",
        }
        thread_pool = []
        ret_music_list = []
        ret_errors = []

        for source_key in sources_list:
            if not source_key in sources_list:
                raise ParameterError("Invalid music source.")

            t = threading.Thread(target=self.search_thread, args=(
                sources_map.get(source_key),
                keyword,
                ret_music_list,
                ret_errors,
            ))
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
            t.join()

        click.echo("\n---------------------------")
        # print(ret_errors)

        return ret_music_list


    def search_thread(self, source, keyword, ret_music_list, ret_errors):
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            ret_music_list += addon.search(keyword)
        except (RequestError, ResponseError, DataError) as e:
            ret_errors.append((source, e))
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            ret_errors.append((source, err))
        finally:
            # 放在搜索后输出是为了营造出搜索很快的假象
            click.echo(" %s ..." % colorize(source.upper(), source), nl=False)


    def playlist(self, url) -> list:
        sources_map = {
            "baidu.com": "baidu",
            # "flac": "flac",
            "kugou.com": "kugou",
            "163.com": "netease",
            "qq.com": "qq",
            "xiami.com": "xiami",
        }
        source = [v for k, v in sources_map if k in url][0]
        if not source:
            raise ParameterError("Invalid url.")
        ret_music_list = []
        ret_errors = []
        try:
            addon = importlib.import_module(".addon." + source, __package__)
            ret_music_list = addon.palylist(url)
        except (RequestError, ResponseError, DataError) as e:
            ret_errors.append((source, e))
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            ret_errors.append((source, err))
        finally:
            click.echo(" %s ..." % colorize(source.upper(), source), nl=False)



