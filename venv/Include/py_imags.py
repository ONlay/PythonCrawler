import urllib.request
import socket
import re
import sys
import os

#定义图片保存路径
targetPath = 'E:\\py_project\\img'

def saveImg(path):
    #检测当前根路径是否有效，不存在则新建
    if not os.path.isdir(targetPath):
        os.mkdir(targetPath)
    #设置每个图片的路径
    #获取图片地址最后一个/的位置
    pos = path.rindex('/')

    #img_path[pos+1:]获取/后面的名称，并加入到根路径
    t = os.path.join(targetPath, path[pos+1:])
    return t
if __name__ == '__main__':
    #需要抓取的url
    url = 'http://movie.douban.com/'
    #添加header文件伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'
    }
    #通过urllib.request获取请求页面数据data
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    data = res.read()

    for link, t in set(re.findall(r'(https:[^s]*?(jpg|png|gif))',str(data))):
        print(link)
        try:
            urllib.request.urlretrieve(link, saveImg(link))
        except:
            print('失败')


