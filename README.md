# music-dl
search and download music 从网易云音乐、QQ音乐、酷狗音乐、百度音乐等搜索和下载歌曲

支持指定搜索数量和音乐源，默认优先尝试下载320K，如果没有320K会下载128K。由于各大音乐网站限制，高品质音乐一般只能通过会员下载。

> 注意：仅支持python3，在python3.7.0运行通过

普通模式：
![](./docs/preview.png)

详细模式：
![](./docs/verbose.png)

## 使用方式
```
$ python main.py -h
usage: python main.py [-k keyword] [-s source] [-c count] [-o outdir] [-v]
	-h --help        帮助
	-v --verbose     详细模式
	-k --keyword=    搜索关键字
	-s --source=     数据源目前支持qq netease kugou
	-c --count=      数量限制
	-o --outdir=     指定输出目录
example: python main.py -k "周杰伦" -s "qq netease kugou" -c 10 -o "/tmp"
```
> 注意：如果经常需要指定数量、目录等参数可以考虑修改glovar.py中的变量

## 支持音乐源列表
已支持
- [x] QQ音乐
- [x] 酷狗音乐
- [x] 网易云音乐
- [x] 百度音乐

待支持
- [ ] 虾米音乐
- [ ] 酷我音乐

欢迎提交插件支持更多音乐源！插件写法参考`core/extractors`中的文件

![](./docs/fork.png)

## 致谢
本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。
- <https://github.com/soimort/you-get>
- <https://github.com/maicong/music>

## LICENSE

WTFPL
