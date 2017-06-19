#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

#qiushibaike#
class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #init header
        self.header = { 'User-Agent' : self.user_agent }
        #cun fang duanzis
        self.stories = []
        #
        self.enable = False

    #pagenumber get page
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers = self.header)
            response = urllib2.urlopen(request)
            #change code to utf-8
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connection error, reason", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "Page load error.."
            return None
        pattern = re.compile('<div.*?author.*?<h2>(.*?)</h2>.*?<div class=.*?content.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        #bianlo
        for item in items:
            #tiaojian
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip()])
        return pageStories

    def loadPage(self):
        #if no-read-pages<2 then load
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            #wait for enter
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"Page%d\tAuthor:%s\n%s" %(page, story[0], story[1])

    def start(self):
        print u"Reading qiushibaike, 'ENTER' to new, Q to quit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()

