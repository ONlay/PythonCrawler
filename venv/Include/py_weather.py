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
                #print(code)
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
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.BadStatusLine as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text
#获取html中我们所需要的字段
def get_data(html_text, city_name):
    #final元组 存放7天的数据
    final = []
    t = []
    t.append(city_name)
    final.append(t)
    bs = BeautifulSoup(html_text, 'html.parser')  #创建BeautifulSoup对象，解析器为：html.parser
    body1 = bs.body  #获取body部分
    #print(body1)
    data = body1.find('div', {'id': '7d'})   #找到id为7d的div
    ul = data.find('ul')
    li = ul.find_all('li')
    for day in li:     #对每一个li标签中的内容进行遍历
        #temp代表每日的数据
        temp = []
        #添加日期
        data = day.find('h1').string   #找到日期
        temp.append(data)   #添加到temp中
        inf = day.find_all('p')    #找到li中的所有的p标签
        #添加天气状况
        temp.append(inf[0].string)     #第一个p标签中的内容（天气状况）加到temp中
        #添加最高气温
        if inf[1].find('span') is None:
            temperature_highest = None
        else:
            temperature_highest = inf[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', '')
        temp.append(temperature_highest)
        #添加最低气温
        temperature_lowest = inf[1].find('i').string
        temperature_lowest = temperature_lowest.replace('℃', '')
        temp.append(temperature_lowest)
        final.append(temp)  #将temp加到final中
    return final
#将抓取到的数据写入文件
def write_data(city_name, data, file_name):
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)
        print('%s 天气已添加成功' %city_name)
if __name__ == '__main__':
    cities = input('请输入城市名称:').split(' ')
    for city in cities:
        url = get_url(city)               #获取城市天气的URL
        html = get_content(url)           #获取网页的HTML
        result = get_data(html, city)     #爬取城市的信息
        write_data(city, result, 'E:\py_project\weather\weather.csv')   #将爬取到的信息填入表格文件

