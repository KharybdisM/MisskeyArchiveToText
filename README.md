# MisskeyArchiveToText

将Misskey的归档文件（json）按年份分割为只包含发表时间、正文、媒体文件的Markdown文件，以提高其可读性。
2024/6/27: 增加了GUI和messagebox提示功能

# Usage

需要安装Python3以执行脚本。

在Misskey账号的`设置-导入和导出`中选择`所有帖子-导出`，在`网盘`一栏内获得本账号下所有贴文归档，归档文件名称形如`notes-20xx-xx-xx-xx-xx-xx.json`

运行程序，选择文件夹内的json文件，按是否下载媒体图片勾选checkbox即可
