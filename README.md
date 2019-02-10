# PixivDownloader

[English](#English) | [中文](#中文)

TODO:

+ [ ] Optimize code
+ [ ] Tag filter
+ [X] Built-in proxy settings

# English

PixivDownloader is a simple batch tool to download all original images of one's on Pixiv.

## Feature

+ Auto-mkdir for individual author
+ Original image
+ Multi-threading support

## Usage

0. Install dependencies `pip install -r requirements.txt`
1. Copy cookies into `main.py` (**Optional to download restricted content** )
2. Execute script
3. Input author user ID (`https://www.pixiv.net/member.php?id=[AUTHOR_UID]`)
3. waiting for `Job finished` prompt and deal with another author

# 中文

PixivDownloader 是一个基于 Python3 的 Pixiv 用户作品多线程批量下载脚本。

## 功能

+ 自动为不同作者建立子目录
+ 下载原始图片
+ 多线程下载

## 使用方法

0. 安装依赖 `pip install -r requirements.txt`
1. 在文件中填入自己的 Cookies （**可选：用于下载限制级内容**）
2. 执行脚本
3. 输入作者的用户 ID （`https://www.pixiv.net/member.php?id=[作者ID]`，作者主页地址的 `id` 参数即为作者用户 ID）
4. 等待 `Job finished` 提示然后输入下一个作者的用户 ID