# @Author  : Austin_Yee
# @Author  : Austin_Yee

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re
import codecs
import time

# 请输入保存路径
save_path = input('请输入保存路径')
# 请输入第一章的网址
url = input('请输入第一章的网址')

# 获得书籍代码和第一章代码
r = re.compile(r'\d+')
s = r.findall(url)
novel_number = s[1]
chapter_number = s[2]

# 请输入需要读取的章节数
chapter_number_str = input('请输入需要读取的章节数，若不输入则为整本（最多为99999999章节）')
if chapter_number_str != '':
    chapterNumberInt = int(chapter_number_str)
else:
    chapterNumberInt = int(99999999)

# 请输入书名
novel_name = input('请输入文件名,若不输入则为书名')


# 保存文件方法
def save(filename, contents):
    fh = open(filename, 'a', encoding='utf-8')
    fh.write(contents)
    fh.close()


# 读取全部章节
for i in range(0, chapterNumberInt):

    try:
        url = f"https://www.9taoxs.com/book/{novel_number}/{chapter_number}.html"  # 基础URL
        head = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'}
        req = urllib.request.Request(url=url, headers=head)  ##封装；一定要有headers，否则不行
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        bs = BeautifulSoup(html, "html.parser")  # 解析文档
        bs = str(bs)

        # 用户是否输入文件名，若无则为书名
        if novel_name == '':
            novel_name = str(re.findall(r'<a href="/book/' + novel_number + r'.html">(.*?)</a>', bs))
            novel_name = novel_name[2:-2]

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
        save(save_path + novel_name + '.txt', story)

        print(head1)

        # 获取下一章地址
        chapter_number1 = re.findall(r'<a href="/book/(.*?)/(.*?).html">下一章【快捷键：→】', bs)
        chapter_number2 = chapter_number1[0]
        chapter_number3 = chapter_number2[1]
        chapter_number4 = re.findall(r'\d+', chapter_number3)
        chapter_number = chapter_number4[-1]

        # 进入下一个循环
        i = i + 1

    except Exception as ex:
        if str(ex) == 'list index out of range':
            break
        print('发生错误，休息10秒再次开始')
        time.sleep(10)
        continue
