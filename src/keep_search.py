import os
import requests
import re
from bs4 import BeautifulSoup
import json
import urllib
import bs4
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getNextPage(url,tags):
    item = json.loads(url)
    nextPage = 'https://api.gotokeep.com/social/v3/hashtag/'+tags+'/timeline?lastId='+item.get("data").get("lastId")+'&sort=heat'
    return nextPage

def downloadPic(url,path):
    r = requests.get(url)
    with open(path+url.split('/')[-1],'wb') as f:
        f.write(r.content)
        f.close()

def main():
    storagePath = 'e:/nowcoder/spider_data'
    folderName = 'keep_search'
    os.chdir(storagePath)
    os.makedirs('keep_search', exist_ok=True)
    print('输入爬取页数')
    total_page = input()
    url = 'https://api.gotokeep.com/social/v3/hashtag/'
    print('输入关键字')
    tags = input()
    tags = urllib.parse.quote(tags)
    url = url + tags + '/timeline?sort=heat'
    for i in range(int(total_page)):
        html = getHTMLText(url)
        #print(html)
        postPageList = []
        detailPage = json.loads(html).get("data").get("results")
        lenth = len(detailPage)
        for j in range(lenth):
            #print(json.loads(html))
            if 'photo' in detailPage[j]:
                item = detailPage[j].get("photo")
                postPageList.append(item)
            for postPage in postPageList:
                downloadPic(postPage,storagePath+'/'+folderName+'/')
        url = getNextPage(html,tags)
        #print(url)
        print("爬取第{0}页面照片数为{1}".format(i+1,len(postPageList)))

main()