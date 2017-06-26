#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

#deal with biaoqian
class Tool:
    removeImg = re.compile('<img.*?>| {7}')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('(<br>){2}|<br>')
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

#baidutieba tiezi
class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"baidutieba"
        self.floorTag = floorTag
        self.num = 0
        self.path = ""

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect baidu-tieba error..Reason",e.reason
                return None

    def getTitle(self, page):
        pattern = re.compile('<h\d.*?>(.*?)</h\d>', re.S)
        result = re.search(pattern, page)
        if result:
            #print result.group(1)
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            #print result.group(1)
            return result.group(1).strip()

    #save image
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def getContent(self, page):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>', re.S)
        picpattern = re.compile('<img.*?src="(.*?)"', re.S)

        items = re.findall(pattern, page)
        #for item in items:
        #   print items[1].strip()
        contents = []
        for item in items:
            self.num += 1
            picitems = re.findall(picpattern, item)
            imagenum = 1
            for picitem in picitems:
                fileName = str(self.num) + '-' + str(imagenum) + '.jpg'
                self.saveImg(picitem, self.path + "/" + fileName)
                imagenum += 1
            content = self.tool.replace(item)
            contents.append(content.encode('utf-8'))
        return contents

    def setFileTitle(self, title):
        if title is not None:
            filename = self.path + "/" + title + ".txt"
            #self.file = open(filename, "w+")
        else:
            pass
            
            #self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + "--\n"
                self.file.write(floorLine)
            self.file.write(item + "\n")
            self.floor += 1
        self.file.write(str(self.floor))

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.mkdir(title)
        self.path = title
        self.setFileTitle(title)
        if pageNum == None:
            print u"URL failed"
            return
        try:
            for i in range(1, int(pageNum)+1):
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print u"Write file error, reason" + e.message
        finally:
            print "Successful"

baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = 0
floorTag = '1'
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()
