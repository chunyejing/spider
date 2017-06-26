#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

class BDTB:

    def __init__(self, baseurl, seelz, savetext):
        self.baseurl = baseurl
        self.seelz = '?see_lz=' + str(seelz)
        self.path = ""
        self.num = 0
        self.savetext = str(savetext)

        #self.tool = Tool()

    def getPage(self, url, pageindex):
        try:
            url = url + self.seelz + '&pn=' + str(pageindex)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect baidu-tieba error..Reason",e.reason
                return None

    def getContents(self, page):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            #print item[0], item[1]
            #contents.append([item[0], item[1]])
            contents.append(item.encode('utf-8'))
        return contents
    
    def getTitle(self, page):
        pattern = re.compile('<h\d.*?>(.*?)</h\d>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()

    def searchImagesAndLinks(self, contents, tag):
        tail = '.jpg'
        picpattern = re.compile('<img.*?src="(.*?)"', re.S)
        linkspattern = re.compile('<a.*?>(.*?)</a>', re.S)
        links = []
        for content in contents:
            self.num += 1
            picitems = re.findall(picpattern, content)
            link = re.findall(linkspattern, content)
            if link:
                links.append(link)
            imagenum = 1
            for picitem in picitems:
                fileName = tag + "/" + str(self.num) + '-' + str(imagenum) + tail
                self.saveImage(picitem, fileName)
                imagenum += 1
        return links

    def saveImages(self, contents, tag):
        tail = '.jpg'
        picpattern = re.compile('<img.*?src="(.*?)"', re.S)
        for content in contents:
            self.num += 1
            picitems = re.findall(picpattern, content)
            imagenum = 1
            for picitem in picitems:
                fileName = tag + "/" + str(self.num) + '-' + str(imagenum) + tail
                self.saveImage(picitem, fileName)
                imagenum += 1

    def saveImage(self, imageurl, filename):
        pass

        u = urllib.urlopen(imageurl)
        data = u.read()
        f = open(filename, 'wb')
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

    def gotoLinks(self, links):
        for link in links:
            for url in link:
                urlpattern = re.compile('.*?baidu.*?', re.S)
                if re.search(urlpattern, url) != None:
                    print url
                    indexPage = self.getPage(url, 1)
                    pageNum = self.getPageNum(indexPage)
                    title = self.getTitle(indexPage)
                    path = self.path + "/" + title
                    self.mkdir(path)
                    if pageNum == None:
                        print u"URL failed"
                        return
                    try:
                        for i in range(1, int(pageNum)+1):
                            page = self.getPage(url, i)
                            contents = self.getContents(page)
                            links = self.saveImages(contents, path)
                            #if self.savetext == '1':
                            #   contents = replace(contents)
                            #   self.writeData(contents)
                    except IOError, e:
                        print u"Write file error, reason" + e.message
                    finally:
                        print "Successful"
          


    def start(self):
        indexPage = self.getPage(self.baseurl, 1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.mkdir(title)
        self.path = title
        if pageNum == None:
            print u"URL failed"
            return
        try:
            for i in range(1, int(pageNum)+1):
                page = self.getPage(self.baseurl, i)
                contents = self.getContents(page)
                links = self.searchImagesAndLinks(contents, title)
                self.gotoLinks(links)
                #if self.savetext == '1':
                #   contents = replace(contents)
                #   self.writeData(contents)
        except IOError, e:
            print u"Write file error, reason" + e.message
        finally:
            print "Successful"

baseurl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seelz = raw_input(u'seelz?(0/1)')
#savetext = raw_input(savetext?(0/1))
savetext = 0
bdtb = BDTB(baseurl, seelz, savetext)
bdtb.start()