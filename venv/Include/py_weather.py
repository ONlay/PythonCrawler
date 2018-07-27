import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

#获取每个城市对应天气的url
def get_url(city_name):
    url = 'http://www.weather.com.cn/weather/'
    with open('E:\py_project\weather\city.txt', 'r', encoding='UTF-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if(city_name in line):
                code = line.split('=')[0].strip()
                return url + code + '.shtml'
    raise ValueError('invalid city name')

#对网页获取get请求，得到的是response对象
def get_content(url, data=None):
    #模拟浏览器访问
    header = {
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Connection': 'keep - alive',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.62 Safari / 537.36'
    }
    #超时，取随机数是因为防止被网站认定为网络爬虫
    timeout = random.choice(range(80, 180))
    while True:
        try:
            #获取请求数据
            rep = requests.get(url, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.error as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

