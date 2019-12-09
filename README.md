# los.py

 一个小脚本, 把从WP页面通过wp助手copy的aria2下载链接转换并通过jsonrpc发送到远程或已启动的aria2服务

- WP/wp: baidu网盘
- wp助手: https://github.com/syhyz1990/baiduyun
- `los` 是德语`losgehen,losfahren`(开始,出发,行动)的简写

## Why do I need this?

- WP助手可以导出(并copy)wp文件的`aria2c`下载命令, 这已经挺方便了. 但是每条命令都会新启动一个aria2c进程, 无法利用当前的aria2c daemon.
- 特别是如果自己有aria2 server, 每次都要ssh进去, 再逐条执行命令
- 如果aria2c 跑在docker里, 就更麻烦, 还有进入docker环境(我的aria2c 在RaspberryPi的docker里)
- 即使通过ssh粘贴并启动aria2c命令, 也无法通过前端(比如ariaNG, webui等)监控下载情况和控制, 因为是不同的aria2c进程.

这个脚本就是解决上述不便, 当aria2c 命令被copy到剪贴板后, 运行脚本, 通过aria2c的jsonrpc,自动在远程aria2 server或者现有进程进行下载, 如果有web前端, 也可监控.

## How does it work?

- 配置好los.py里面的URL,token
- 先从wp助手导出aria2c命令(默认进入剪贴板)
- 直接运行这个los.py, 会自动读取剪贴板, 转换并发送到指定的aria2 server
- 目前只是读取剪贴板的内容, 没做从文件加载, 因为wp助手直接copy很方便

## Tech.

- los.py本身没什么技术含量, 主要工作都是aria2c和wp助手做的
- 依赖: xclip, python-requests
- 只测试了Linux, 别的OS没钱买.
