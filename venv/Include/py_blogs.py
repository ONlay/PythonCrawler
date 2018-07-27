# csdn 博客爬虫
# 日期  主题 链接 访问量 评论个数


import urllib.request
import re
import gzip
from bs4 import BeautifulSoup


# 定义保存文件的函数 整个页面的博客信息加入
def save_File(data, i):
    path = "E:\\py_project\\CSDN\\" + str(i + 1) + ".txt"
    file = open(path, 'wb')
    # 先把页page写进去文件
    page = '当前页：' + str(i + 1) + '\r\n'
    file.write(page.encode('gbk'))
    # 再将博文的日期和访问量等信息写进文件 d代表一个博客信息
    for d in data:
        print(d)
        d = str(d) + '\r\n'  # 加一个隔一行
        file.write(d.encode('gbk'))
    file.close()


#  解压缩数据
def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未压缩，无需解压")
    return data


#  CSDN 爬虫类
class CSNDSpider:
    #  初始化
    def __init__(self, pageIdx=1, url="http://blog.csdn.net/fly_yr/article/list"):
        self.pageIdx = pageIdx
        self.url = url
        self.headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "blog.csdn.net"
        }

    #  求总页数
    def get_page(self):
        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)

        # 从csdn博客主页抓取的内容是压缩后的内容，先解压缩
        data = res.read()
        data = ungzip(data)
        #  用"utf-8"格式编码
        data = data.decode('utf-8')

        #  获取BeautifulSoup对象
        s = BeautifulSoup(data, "html5lib")
        #print(s)
        page_tag = s.find("div", "pageBox")
        #print(page_tag)
        #print(page_tag)
        pagesData = page_tag.li.get_text()
        #  获取总页的正则
        #print(pagesData)
        pagesNum = re.findall(re.compile(pattern=r'共(.*?)页'), pagesData)[0]
        return pagesNum

    #  设置要抓取的页面
    def setPage(self, idx):
        self.url = self.url[0:self.url.rfind('/') + 1] + str(idx)

    #  读取博文信息
    def read_data(self):
        #  ret 元组用来存放博文信息的集合
        ret = []

        req = urllib.request.Request(url=self.url, headers=self.headers)
        res = urllib.request.urlopen(req)

        #  获取博文的信息
        data = res.read()
        # 从csdn博客主页抓取的内容是压缩后的内容，先解压缩
        data = ungzip(data)
        data = data.decode('utf-8')
        # print(data)

        #  创建BeautifuSoup 对象
        s = BeautifulSoup(data, "html5lib")
        #  通过find_all 获取全部 博文一整段的信息
        items = s.find_all('div', "list_item article_item")
        for item in items:
            #  标题
            title = item.find('span', "link_title").a.get_text()
            #  链接
            link = item.find('span', "link_title").a.get("href")
            #  写作时间
            write_time = item.find('span', "link_postdate").get_text()
            #  阅读量  re.compile(r'(.∗?)')正则获取的数据为 “阅读（223）”所以223为[3]
            reader_nums = re.findall(re.compile(r'(.∗?)'), item.find('span', "link_view").get_text())[3]
            #  评论量 re.compile(r'(.∗?)')正则获取的数据为 “评论（2）”所以2为[3]
            comments = re.findall(re.compile(r'(.∗?)'), item.find('span', "link_comments").get_text())[3]

            ret.append('日期：' + write_time + '\r\n' + '标题：' + title
                       + '\r\n' + '链接：http://blog.csdn.net' + link
                       + '\r\n' + '阅读：' + reader_nums + '\t评论：' + comments + '\r\n')
        return ret


if __name__ == '__main__':
    #  定义爬虫对象
    cs = CSNDSpider()
    #  获取页面总数
    pagesNum = int(cs.get_page())
    print("博文总页数：", pagesNum)

    #  循环将每页获取的博文存入本地
    for idx in range(pagesNum):
        # 设置页
        cs.setPage(idx)
        print("当前页：", idx + 1)
        #  获取信息
        page_data = cs.read_data()
        # 将信息存入本地
        save_File(page_data, idx)
