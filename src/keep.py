import os
import requests
import re
from bs4 import BeautifulSoup
import json
import bs4
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getSecondPage(html):
    soup = BeautifulSoup(html,"html.parser")
    #nextId = soup.find_all(class_="keep-loading-more")
    nextId = str(soup.find_all(name ='div',attrs={"data-url":re.compile(r'^/explore/more\?lastId=')})[0])
    suffix = nextId[nextId.index('/explore'):-8]
    nextPage = 'http://www.gotokeep.com' + suffix
    return nextPage

def getNextPage(url):
    #pageDetail = getHTMLText(url)
    #print(url)
    item = json.loads(url)
    nextPage =  'http://www.gotokeep.com/explore/more?lastId='+ item.get("data").get("lastId")
    return nextPage

def getPostPage(html):
    soup = BeautifulSoup(html,"html.parser")
    postPageList = soup.find_all(name = 'a',attrs={"sensor-item-reason":"hotEntryTimeline"})
    return postPageList
    # for item in postPage:
    #     print(item.get("href"))

def getPicPage(postPage):
    html = getHTMLText(postPage)
    soup = BeautifulSoup(html, "html.parser")
    picPageList = soup.find_all(name = 'img',class_="entry-pic")
    return picPageList

def downloadPic(url,path):
    r = requests.get(url)
    with open(path+url.split('/')[-1],'wb') as f:
        f.write(r.content)
        f.close()

def main():
    storagePath = 'e:/nowcoder/spider_data'
    folderName = 'keep'
    os.chdir(storagePath)
    os.makedirs('keep', exist_ok=True)
    print('输入爬取页数')
    total_page = input()
    url = 'http://www.gotokeep.com/explore'
    for i in range(int(total_page)):
        html = getHTMLText(url)
        if i==0:
            postPageList = getPostPage(html)
        else:
            postPageList = getPostPage(json.loads(html).get("data").get("html"))
        for postPage in postPageList:
            picPageList = getPicPage("http://www.gotokeep.com"+postPage.get("href"))
            for item in picPageList:
                downloadPic(item.get("src"),storagePath+'/'+folderName+'/')
        if i==0:
            url = getSecondPage(html)
        else:
            url = getNextPage(html)
        print("爬取第 %d 页完成" % i)

main()