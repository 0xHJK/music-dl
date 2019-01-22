# music-dl
从网易云音乐、QQ音乐、酷狗音乐、百度音乐、虾米音乐等搜索和下载歌曲。

支持指定搜索数量和音乐源，默认优先尝试下载320K，如果没有320K会下载128K。

由于各大音乐网站限制，高品质音乐一般只能通过会员下载。

> 注意：部分音乐源在一些国家和地区不可用，可以考虑使用中国大陆代理。
>

Search and download music from netease, qq, kugou, baidu and xiami.

You can specify music sources and limit count of search results. 

The default priority is to try to download 320K music, then 128K.

> Note: Some music sources may not be available in some countries and regions. If so, you can use Chinese proxies.

在以下环境测试通过（仅支持Python3）：

| 系统名称 | 系统版本      | Python版本 |
| -------- | ------------- | ---------- |
| macOS    | 10.14         | 3.7.0      |
| macOS    | 10.13         | 3.7.0      |
| Windows  | Windows 7 x64 | 3.7.2      |
| Ubuntu   | 16.04 x64     | 3.5.2      |

## 免责声明

- 本工具只用作个人学习研究，禁止用于商业及非法用途，如产生法律纠纷与本人无关。
- API来自网络，非官方API，随时可能失效。
- 音乐版权归各网站所有，本工具主要目的是协助搜索，发现哪家音乐有版权。
- 音乐仅用于试听，如果需要保存，请自行去各个网站下载正版。

## Usage 使用方式

安装依赖：

```
$ pip3 install -r requirements.txt
```

使用帮助：

```
$ python3 main.py -h
usage: python main.py [-k keyword] [-s source] [-c count] [-o outdir] [-v] [-m]
	-h --help        帮助
	-v --verbose     详细模式
	-m --merge       对搜索结果去重和排序
	--nomerge        对搜索结果不去重（默认不去重）
	-k --keyword=    搜索关键字
	-s --source=     数据源目前支持qq netease kugou baidu xiami
	-c --count=      数量限制
	-o --outdir=     指定输出目录
example: python main.py -k "周杰伦" -s "qq netease kugou baidu xiami" -c 10 -o "/tmp"
```

默认搜索所有音乐源，每个数量限制为5，保存目录为当前目录，不合并搜索结果。

指定序号时可以使用`1-5 7 10`的形式。

合并搜索结果时，排序顺序按照歌手和歌名排序，当两者都相同时保留最大的文件。

> 注意：如果经常需要指定数量、目录等参数可以考虑修改glovar.py中的变量

Example 使用示例：

![](./docs/preview.png)

去重效果展示：

Before merge 去重前：

![](./docs/normal.png)

After merge 去重后：

![](./docs/merge.png)

## Music sources 支持音乐源列表
| 音乐源     | 缩写    | 网址                    |
| ---------- | ------- | ----------------------- |
| QQ音乐     | qq      | <https://y.qq.com/>     |
| 酷狗音乐   | kugou   | <http://www.kugou.com/> |
| 网易云音乐 | netease | <https://music.163.com/>  |
| 百度音乐   | baidu   | <http://music.baidu.com/> |
| 虾米音乐   | xiami   | <https://www.xiami.com/>  |

欢迎提交插件支持更多音乐源！插件写法参考`core/extractors`中的文件

![](./docs/fork.png)

## Credits 致谢
本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。
- <https://github.com/soimort/you-get>
- <https://github.com/maicong/music>

## LICENSE

WTFPL
