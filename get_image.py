#导入需要的库
import urllib
import urllib.request
import os
import re
import time
#主要流程:获取网址源码→获取源码里图片地址→根据地址循环下载图片
#一、获取网址源码
def get_html(httpurl):
     page = urllib.request.urlopen(httpurl)#利用方法打开http地址
     html_code = page.read()#将内容读取到对象(此时是二进制编码)
     return html_code#返回得到的源码
#二、获取源码里的图片地址
def get_keywd_urllist(keywd):
     keywd = urllib.parse.quote(keywd)#将关键字转为ASCII码
     search_url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word='#搜索地址为百度图片地址(此为固定地址)
     search_url = search_url + keywd#将固定地址和关键词拼接成搜索地址
     htmlcode = get_html(search_url)#调用前面的函数获得地址里的源码(注意此时是二进制编码)
     html_str = htmlcode.decode(encoding='utf-8')#利用decode方法转换为utf-8编码
     reg_str = r'"objURL":"(.*?)",'#根据得到的源码找到图片地址并编写正则表达式
     reg_compile = re.compile(reg_str)#编译正则表达式，得到一个模式对象
     image_list = reg_compile.findall(html_str)#图片地址=正则表达式.寻找(源码)
     return image_list
#三、下载图片
keywd = input('请输入关键词：')
pic_list = get_keywd_urllist(keywd)
x=0
print('<<<<<获取图片地址>>>>>')
for pic in pic_list:
     if pic[len(pic)-1] == 'g':
         print(pic)
         name = keywd + str(x)
         time.sleep(0.01)
         print('<<<<<图片下载中>>>>>')
         if os.path.exists("./image"):
            urllib.request.urlretrieve(pic, './image/%s.jpg'%name)
         else:
             os.mkdir("./image")
             urllib.request.urlretrieve(pic, './image/%s.jpg' % name)
         x+=1
