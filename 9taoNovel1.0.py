# @Author  : Austin_Yee

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re
import codecs
import time
import random

# 请输入书籍地址
novelNumber = input('请输入书籍地址')

# 请输入第一章地址
urlNumber = input('请输入第一章地址')

# 请输入需要读取的章节数
chapterNumberStr = input('请输入需要读取的章节数')
chapterNumberInt = int(chapterNumberStr)

# 保存文件方法
def save(filename, contents):
    fh = open(filename, 'a', encoding='utf-8')
    fh.write(contents)
    fh.close()

# 读取全部章节
for i in range (0,chapterNumberInt):

    url = f"https://www.9taoxs.com/book/{novelNumber}/{urlNumber}.html"  # 基础URL
    head = {'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'}
    req = urllib.request.Request(url=url, headers=head)  ##封装；一定要有headers，否则不行
    res = urllib.request.urlopen(req)
    html = res.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")  # 解析文档
    bs = str(bs)

    # 读取标题
    head1 = re.findall(r'<h1>(.*?)</h1>', bs)
    # 去除多余符号
    if head1[:3] == codecs.BOM_UTF8:
        head1 = head1[3:]

    # 读取正文
    paragraph1 = re.findall(r'<p>(.*?)</p>', bs)
    # 去除多余符号
    if paragraph1[:3] == codecs.BOM_UTF8:
        paragraph1 = paragraph1[3:]

    # 写入txt
    story1 = '\n'.join(head1)
    story2 = '\n'.join(paragraph1)
    story = story1 + '\n' + story2
    save(r'C:\Users\17106\Desktop\file1.txt', story)

    print(head1)

    # 获取下一章地址
    urlNumber1 = re.findall(r'<a href="/book/(.*?)/(.*?).html">下一章【快捷键：→】',bs)
    urlNumber3 = urlNumber1[0]

    urlNumber4 = urlNumber3[1]
    urlNumber = urlNumber4[-7:-1] + urlNumber4[-1]

    time.sleep(random.random()*2)

    # 进入下一个循环
    i=i+1
