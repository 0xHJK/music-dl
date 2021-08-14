# Music-dl: Listen to what you want

<p align="center">
  <a href="https://github.com/0xHJK/music-dl">
    <img src="https://github.com/0xHJK/music-dl/raw/master/static/logo.png" height="400" alt="music-dl">
  </a>
</p>
<hr>
<p align="center">
  <a href="https://travis-ci.org/0xHJK/music-dl">
    <img src="https://travis-ci.org/0xHJK/music-dl.svg?branch=master">
  </a>
  <a><img src="https://img.shields.io/pypi/pyversions/pymusic-dl.svg"></a>
  <a href="https://codecov.io/gh/0xHJK/music-dl">
    <img src="https://codecov.io/gh/0xHJK/music-dl/branch/master/graph/badge.svg"/>
  </a>
  <a href="https://github.com/0xHJK/music-dl/releases">
    <img src="https://img.shields.io/github/release/0xHJK/music-dl.svg">
  </a>
  <a><img src="https://img.shields.io/github/license/0xHJK/music-dl.svg"></a>
</p>

**[Music-dl](https://github.com/0xHJK/music-dl)** is a command line tool which helps you search and download music from multiple sources.

Support for QQ music, Netease music, Xiami music, Kugou music and Baidu music. See [supported sources](#支持的音乐源列表).

**Python3 Only. Python 3.5+ Recommended.**

[English](https://github.com/0xHJK/music-dl/blob/master/README.en.md) | 中文文档

**[Music-dl](https://github.com/0xHJK/music-dl)
**是一个基于Python3的命令行工具，可以从多个网站搜索和下载音乐，方便寻找音乐，解决不知道哪个网站有版权的问题。工具的本意是**聚合搜索**，API
是从公开的网络中获得，**不是破解版**，也听不了付费歌曲。

**禁止将本工具用于商业用途**，如产生法律纠纷与本人无关，如有侵权，请联系我删除。

微博：[可乐芬达王老吉](https://weibo.com/p/1005056970125848/home?is_all=1)

QQ群：[785798493](//shang.qq.com/wpa/qunwpa?idkey=ead6a77d50b8dbaa73cf78809aca0bd20c306b12f9984a17436f0342b1c0d65c)

最近API封杀有点多，个人有点维护不过来，需要大家帮忙更新。查看 [支持的音乐源列表](#支持的音乐源列表)

> 注意: 部分音乐源在一些国家和地区不可用，可以考虑使用中国大陆代理。获取公共代理的方式可以参考我的另一个项目<https://github.com/0xHJK/Proxies>，两分钟获得数千个有效代理。

## 功能

- 部分歌曲支持无损音乐
- 优先搜索高品质音乐（无损 -> 320K -> 128K）
- 支持 HTTP 和 SOCKS 代理
- 支持多线程搜索
- 支持搜索结果去重和排序
- 支持搜索关键字高亮
- 支持下载歌词和封面（部分）

> 注意：仅支持Python3，建议使用 **Python3.5 以上版本**

## 安装

使用pip安装（推荐，注意前面有一个`py`）：

```bash
$ pip3 install pymusic-dl
```

手动安装（最新）：

```bash
$ git clone https://github.com/0xHJK/music-dl.git
$ cd music-dl
$ python3 setup.py install
```

不安装直接运行：

```bash
$ git clone https://github.com/0xHJK/music-dl.git
$ cd music-dl
$ pip3 install -r requirements.txt
$ ./music-dl

# 或 python3 music-dl
```

在以下环境测试通过：

| 系统名称 | 系统版本       | Python版本 |
| -------- | -------------- | ---------- |
| macOS    | 10.14          | 3.7.0      |
| macOS    | 10.13          | 3.7.0      |
| Windows  | Windows 7 x64  | 3.7.2      |
| Windows  | Windows 10 x64 | 3.7.2      |
| Ubuntu   | 16.04 x64      | 3.5.2      |

## 使用方式

v3.0预览版命令有较大的改变，建议先查看帮助

```
$ music-dl --help
Usage: music-dl [OPTIONS]

  Search and download music from netease, qq, kugou, baidu and xiami.
  Example: music-dl -k "周杰伦"

Options:
  --version             Show the version and exit.
  -k, --keyword TEXT    搜索关键字，歌名和歌手同时输入可以提高匹配（如 空帆船 朴树）
  -u, --url TEXT        通过指定的歌曲URL下载音乐
  -p, --playlist TEXT   通过指定的歌单URL下载音乐
  -s, --source TEXT     Supported music source: qq netease kugou baidu
  -n, --number INTEGER  Number of search results
  -o, --outdir TEXT     Output directory
  -x, --proxy TEXT      Proxy (e.g. http://127.0.0.1:1087)
  -v, --verbose         Verbose mode
  --lyrics              同时下载歌词
  --cover               同时下载封面
  --nomerge             不对搜索结果列表排序和去重
  --help                Show this message and exit.
```

- 默认搜索`qq netease kugou baidu `，每个数量限制为5，保存目录为当前目录。
- 指定序号时可以使用`1-5 7 10`的形式。
- 默认对搜索结果排序和去重，排序顺序按照歌手和歌名排序，当两者都相同时保留最大的文件。
- 无损音乐歌曲数量较少，如果没有无损会显示320K或128K。
- 支持http代理和socks代理，格式形如`-x http://127.0.0.1:1087`或`-x socks5://127.0.0.1:1086`

示例：

![](https://github.com/0xHJK/music-dl/raw/master/static/preview.png)

## 支持的音乐源列表

| 音乐源     | 缩写    | 网址                      | 有效 | 无损 | 320K | 封面 | 歌词 | 歌单 | 单曲 |
| ---------- | ------- | ------------------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| QQ音乐     | qq      | <https://y.qq.com/>       | ✓     | -    | -    | ✕    | ✓     | ✕    | ✕    |
| 酷狗音乐   | kugou   | <http://www.kugou.com/>   | ✓     | -    | -    | -    | ✕    | -    | ✕    |
| 网易云音乐 | netease | <https://music.163.com/>  | ✓    | -    | ✓    | ✓    | ✓    | ✓    | ✓    |
| 咪咕音乐   | migu    | <http://www.migu.cn/>     | ✓    | ✓    | ✓    | ✓    | ✓    | ✕    | ✕    |
| 百度音乐   | baidu   | <http://music.baidu.com/> | ✓    | -    | ✓    | ✓    | ✓    | ✕    | ✕    |
| 虾米音乐   | xiami   | <https://www.xiami.com/>  | ✕    | -    | -    | -    | -    | ✕    | ✕    |

> `-`表示不一定支持，`✓`表示部分或完全支持，`✕`表示尚未支持

欢迎提交插件支持更多音乐源！插件写法参考`addons`中的文件

![](https://github.com/0xHJK/music-dl/raw/master/static/fork.png)

## 更新记录

- 2019-08-25 修复了QQ音乐、网易云音乐、酷狗音乐，新增咪咕音乐
- 2019-08-03 修复了一些bug，屏蔽了不支持的源，目前仅百度音乐可用
- 2019-06-13 重新增加虾米音乐高品质音乐支持，感谢群友0.0提供的API
- 2019-06-11 v3.0预览版，代码重构，支持网易云音乐歌单和单曲下载，支持百度高品质音乐
- 2019-04-08 发布v2.2.1版本
- 2019-04-04 因为虾米音乐API变更，暂时屏蔽虾米搜索结果#22
- 2019-04-02 修复#18和#21的BUG，优化显示效果，支持部分音乐源歌词和封面下载
- 2019-03-11 开启默认支持所有音乐源，默认对搜索结果排序去重，优化显示效果，高亮搜索关键字和高品质音乐
- 2019-02 完成部分翻译（英语、德语、日语、克罗地亚语）感谢@anomie31 @DarkLinkXXXX @terorie的帮助，目前翻译尚未完善，欢迎提交PR改进翻译
- 2019-01-31 新增单元测试，集成发布，新增LOGO，新增小徽章，发布v2.1.0版本
- 2019-01-28 重写一半以上代码，全面优化，发布到pip库，发布v2.0.0版本
- 2019-01-26 支持http和socks代理，删除wget库，新增click库，发布v1.1版
- 2019-01-25 支持百度无损音乐
- 2019-01-24 优化交互、修复bug
- 2019-01-22 解决Windows兼容问题，支持多线程，发布v1.0版
- 2019-01-21 支持虾米音乐，支持去重
- 2019-01-20 支持百度音乐
- 2019-01-17 支持指定目录、数量、音乐源
- 2019-01-12 QQ音乐320K失效
- 2019-01-11 支持网易云音乐
- 2019-01-09 完成v0.1版，支持酷狗和QQ

## 提Issues说明

- **检查是否是最新的代码，检查是否是Python3.5+，检查依赖有没有安装完整**。
- 说明使用的操作系统，例如Windows 10 x64
- 说明Python版本，以及是否使用了pyenv等虚拟环境
- 说明使用的命令参数、搜索关键字和出错的音乐源
- 使用`-v`参数重试，说明详细的错误信息，最好有截图
- 如果有新的思路和建议也欢迎提交

## Credits 致谢

本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。

- <https://github.com/requests/requests>
- <https://github.com/soimort/you-get>
- <https://github.com/maicong/music>
- <https://github.com/YongHaoWu/NeteaseCloudMusicFlac>
- <https://github.com/darknessomi/musicbox>

## 用爱发电

维护不易，欢迎扫描恰饭二维码

![](https://github.com/0xHJK/music-dl/raw/master/static/wepay.jpg)

## LICENSE

[MIT License](https://github.com/0xHJK/music-dl/blob/master/LICENSE)
