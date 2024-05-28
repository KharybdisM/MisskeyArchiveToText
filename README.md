# MisskeyArchiveToText

一个将Misskey的归档文件（json）按年份分割为只包含发表时间、正文、媒体文件的Markdown文件，以提高其可读性。

# Usage

需要安装Python3以执行脚本。

在Misskey账号的`设置-导入和导出`中选择`所有帖子-导出`，在`网盘`一栏内获得本账号下所有贴文归档，归档文件名称形如`notes-20xx-xx-xx-xx-xx-xx.json`

将`misskey2text.py`放入归档文件所在的文件夹中，在终端中输入：

```
python --j misskey2text.py
```

此命令将按年份分割贴文并进行归档，并将所有媒体文件下载至本地文件夹`media`中，md文件内的图片地址为本地地址。

如果不希望下载图片，只需要存档文字（媒体文件直接引用网络地址），请使用以下命令：

```
python --j misskey2text.py --p n
```

此命令仅按年份分割贴文并进行归档，不下载媒体文件到本地。

生成的md文件可用任意Markdown编辑器打开。
