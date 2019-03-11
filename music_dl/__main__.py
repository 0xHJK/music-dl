#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: main.py
@time: 2019-01-08
"""

import sys
import re
import threading
import click
import logging
import prettytable as pt
from . import config
from .utils import colorize
from .core import music_search, music_download, music_list_merge, get_sequence

import gettext
gettext.install('music-dl', 'locale')

def run():
    logger = logging.getLogger(__name__)
    music_list = []
    thread_pool = []
    errors = []

    click.echo(
        "\n"
        + _("正在搜索 {searchterm} 来自 ...").format(
            searchterm=colorize(config.get("keyword"), "yellow")
        ),
        nl=False,
    )

    # 多线程搜索
    for source in config.get("source").split():
        t = threading.Thread(target=music_search, args=(source, music_list, errors))
        thread_pool.append(t)
        t.start()
    for t in thread_pool:
        t.join()

    # 分割线
    click.echo("\n---------------------------\n")
    # 输出错误信息
    for err in errors:
        logger.debug(_("音乐列表 {error} 获取失败.").format(error=err[0].upper()))
        logger.debug(err[1])
    # 对搜索结果排序和去重
    if config.get("merge"):
        music_list = music_list_merge(music_list)
    # 创建table
    tb = pt.PrettyTable()
    tb.field_names = ["序号", "歌手", "歌名", "大小", "时长", "专辑", "来源"]
    # 遍历输出搜索列表
    for index, music in enumerate(music_list):
        music.idx = index
        tb.add_row(music.row)
        # click.echo(music.info)
    tb.align = "l"
    click.echo(tb)

    # 分割线
    click.echo("\n---------------------------")
    # 用户指定下载序号
    prompt = (
        _("请输入{下载序号}，支持形如 {numbers} 的格式，输入 {N} 跳过下载").format(
            下载序号=colorize(_("下载序号"), "yellow"),
            numbers=colorize("0 3-5 8", "yellow"),
            N=colorize("N", "yellow"),
        )
        + "\n >>"
    )

    choices = click.prompt(prompt)
    while choices.lower() != "n" and not re.match(
        r"^((\d+\-\d+)|(\d+)|\s+)+$", choices
    ):
        choices = click.prompt("%s%s" % (colorize(_("输入有误!"), "red"), prompt))

    selected_list = get_sequence(choices)
    for idx in selected_list:
        music_download(idx, music_list)

    # 下载完后继续搜索
    keyword = click.prompt(_("请输入要搜索的歌曲，或Ctrl+C退出") + "\n >>")
    config.set("keyword", keyword)
    run()


@click.command()
@click.version_option()
@click.option(
    "-k",
    "--keyword",
    prompt=_("请输入要搜索的歌曲，名称和歌手一起输入可以提高匹配（如 空帆船 朴树）") + "\n >>",
    help=_("搜索关键字"),
)
@click.option(
    "-s",
    "--source",
    default="qq netease kugou baidu xiami flac",
    help=_("支持的数据源: ") + "qq netease kugou baidu xiami flac",
)
@click.option("-c", "--count", default=5, help=_("搜索数量限制"))
@click.option("-o", "--outdir", default=".", help=_("指定输出目录"))
@click.option("-x", "--proxy", default="", help=_("指定代理（如http://127.0.0.1:1087）"))
@click.option("-m", "--merge", default=True, is_flag=True, help=_("对搜索结果去重和排序（默认去重）"))
@click.option("-v", "--verbose", default=False, is_flag=True, help=_("详细模式"))
def main(keyword, source, count, outdir, proxy, merge, verbose):
    """
        Search and download music from netease, qq, kugou, baidu and xiami.
        Example: music-dl -k "周杰伦"
    """
    # 初始化全局变量
    config.init()
    config.set("keyword", keyword)
    config.set("source", source)
    config.set("count", min(count, 50))
    config.set("outdir", outdir)
    config.set("merge", merge)
    config.set("verbose", verbose)
    if proxy:
        proxies = {"http": proxy, "https": proxy}
        config.set("proxies", proxies)

    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)-8s | %(name)s: %(msg)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        run()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)


if __name__ == "__main__":
    main()
