import re
import urllib2

class HTML_Tool:

    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")


    EndCharToNoneRex = re.compile("<.*?>")


    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")


    replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]

    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n   ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:
            x = x.replace(t[0],t[1])
        return x

class Baidutieba_spider:
    def __init__(self, url):
        self.url = url
        self.html_dealer = HTML_Tool()

    def start(self):
        Page = urllib2.urlopen(self.url).read()
        title = self.get_title(Page)
        pagenum = self.get_pagenum(Page)
        filename = 'Baidu.txt'
        f = open(filename, 'a')
        f.write(title)
        f.close()
        self.save_file(filename, pagenum)

    def get_title(self, Page):
        pattern = '<h3.*?>(.*?)</h3>'
        title = re.search(pattern, Page, re.S).group(1)
        if title:
            print 'title:', title
        else:
            print 'failed to get title'
        return title

    def get_pagenum(self, Page):
        pattern = 'class="red">(\d+)</span>'
        pagenum = int(re.search(pattern, Page, re.S).group(1))
        if pagenum:
            print 'It contains %d pages.' % pagenum
        else:
            print 'failed to get the number of pages.'
        return pagenum

    def save_file(self, filename, pagenum):
        for i in range(1, pagenum + 1):
            fullurl = self.url + '&pn=%d' % i
            Page = urllib2.urlopen(fullurl).read()
            pattern = 'id="post_content.*?>(.*?)</div>'
            Items = re.findall(pattern, Page, re.S)
            f = open(filename, 'a')
            print 'saving page %d...' % i
            for item in Items:
                s = self.html_dealer.Replace_Char(item)
                f.write(s)
                f.write('\n')
            f.close()


my_spider = Baidutieba_spider(raw_input('Please enter the url:'))
my_spider.start()

















