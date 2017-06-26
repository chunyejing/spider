#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

class Spider:
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageindex):
        url = self.siteURL + '?page=' + str(pageindex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, pageindex):
        page = self.getPage(pageindex)
        pattern = re.compile('<a class="lady-name" href="(.*?)".*?>(.*?)</a>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            #print item[0], item[1]
            contents.append([item[0], item[1]])
        return contents

    def gotoTaobao(self, url):
        response = urllib2.urlopen(url)
        print url
        return response.read().decode('gbk')

    def gotoCenter(self, page):
        print page
        pattern = re.compile('<div.*?domain.*?<span>(.*?)</span>', re.S)
        centerurl = re.search(pattern, page)
        print centerurl
        response = urllib2.urlopen('http:' + centerurl.group(1).strip())
        return response.read().decode('gbk')
        
    def getText(self, page):
        pass

    def getAllImage(self, page):
        pattern = re.compile('<img.*?src="(.*?)"',re.S)
        images = re.findall(pattern, page)
        return images

    def saveImgs(self, images, tag):
        number = 1
        fTail = 'jpg'
        for imageurl in images:
            filename = tag + "/" + str(number) + "." +fTail
            self.saveImg(imageurl, filename)
            number += 1

    def saveImg(self, imageurl, filename):
        u = urllib.urlopen(imageurl)
        data = u.read()
        f = open(filename, 'wb')
        f.write(data)
        f.close()

    def saveText(self, content, name):
        filename = name + "/" + name + ".txt"
        f = open(filename, 'w+')
        #print content.encode('utf_8')
        f.write(content.encode('utf_8'))

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False
    
    def savePageInfo(self, pageindex):
        contents = self.getContents(pageindex)
        for item in contents:
            name = item[1]
            personalurl = 'http:' + item[0]
            personalpage = self.gotoTaobao(personalurl)
            centerpage = self.gotoCenter(personalpage)
            images = self.getAllImage(centerpage)
            self.mkdir(name)
            self.saveImgs(images, name)

    def savePagesInfo(self, start, end):
        for i in range(start, end+1):
            self.savePageInfo(i)

spider = Spider()
spider.savePagesInfo(1, 1)