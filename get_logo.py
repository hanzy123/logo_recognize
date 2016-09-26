# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 10:26:42 2016

@author: mac
"""
import urllib
import re
import os
import socket
def schedule(a,b,c):
  '''''
  a:已经下载的数据块
  b:数据块的大小
  c:远程文件的大小
   '''
  per = 100.0 * a * b / c
  if per > 100 :
    per = 100
  print '%.2f%%' % per

def getHtml(url):
  page = urllib.urlopen(url)
  html = page.read()
  return html
def downloadImg(html,logoname,count):
  reg = r'"objURL":"(.*?)"'
  imgre = re.compile(reg)
  imglist = re.findall(imgre, html)
  #定义文件夹的名字
  picpath = 'logo_img/%s/' % (logoname) #下载到的本地目录
  
  if not os.path.exists(picpath):   #路径不存在时创建一个
    os.makedirs(picpath)   
  x = 0
  socket.setdefaulttimeout(10)#设置防止下载时间超时
  for imgurl in imglist:
    target = picpath+'%s.jpg' % count
    print 'Downloading image to location: ' + target + '\nurl=' + imgurl
    try:    
        image = urllib.urlretrieve(imgurl, target, schedule)
        x += 1
        count += 1
        print "count =========" + str(count)
    except:
        continue
  return image,count;
if __name__ == "__main__":
    f = open("logo_name1.txt", "r")  
    while True:
        logoname = f.readline()
        logoname = logoname[:-1]
        page = 0;
        if logoname:
            count = 0
            try:
                while(count<400):#设置需要下载图片的数目
                    html = getHtml("http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%d"%(logoname,page))          
                    image,count = downloadImg(html,logoname,count)
                    page += 20
            except:
                continue
        else:
            break
    print "Download has finished."