# 爬虫练手

标签（空格分隔）： 网络爬虫 requests BeautifulSoup pyspider

---

## 项目简介 ##

 - 爬取v2ex帖子内容及用户回复
 - 爬取网页版keep热门内容
 - 按关键词爬取网页版keep热门内容


----------
## 爬取v2ex ##
该爬虫采用[pyspider](http://www.pyspider.cn/index.html)框架，爬取中的帖子内容及回复内容，将爬取到的数据存入MySQL数据库中，供项目[demo3](https://github.com/WinterYuan/demo3)调用。主要通过正则表达式查找匹配的连接，然后调用pyspider的self.crawl()API进行跳转，详细API可参考pyspiderAPI说明文档。数据库表单结构如下：

**question table**

| id | title | content | user_id | created_data | comment_count |
| -------- | :----: | :----: | :----: | :----: | :----: |
| 3610 | 升级 10.10.3 后开机慢了 | 昨天手贱升级了10.10.3，发现开机的时候慢得不行啊，以后一开机就出现白苹果logo，现在硬生生等了20秒左右才出现logo。大家有没有这样的情况？PS：话说苹果这货出个系统是越出越占资源，而微软是把系统越做越少占资源的，越多地考虑那些老机器。之前没用苹果之前，看大家神化成这样，买了回来，发现实际上也就是上面的app简洁一点，系统和硬件结合比较好罢了，系统好用还真没觉得。 | 5 | 2018-01-19 20:11:33 | 17 |

**comment table**

| id | content | uer_id | entity_id | entity_type | created_date | status | 
| -------- | :----: | :----: | :----: | :----: | :----: | :----: |
| 1 | 我的MBA升级10.10.3之后，开机也明显变慢了。另外，Cisco AnyConnect Secure Mobility Client 也受限没法用了。 | 2 | 3610 | 1 | 2018-01-19 20:11:33 | 0 |

## 爬取keep热门内容 ##
爬虫练手项目，主要是为了熟悉[requests](http://cn.python-requests.org/zh_CN/latest/)库和[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)的使用，熟悉正则表达式。[keep精选][1]采用瀑布流刷新的形式，当鼠标滚动到最底层时自动加载下一页，通过观察网页后台XHR中的Header发现每次请求的新网页地址格式为
http://www.gotokeep.com/explore/more?lastId=
lastId会附在当前加载的html中，所以正则找到lastId即可获取下一跳转界面的URL，注意第一页跳转和后面的跳转URL格式上有所区别，在程序中作了区分。通过BeautifulSoup解析thml界面查找当前页面包含的热门内容，跳转后爬取热门内容的图片。
## 按标签爬取keep热门内容 ##
爬虫练手项目，keep社区可以按照用户发布状态中包含的标签进行过滤，例如标签[我要上精选][2]，URL的格式为
http://www.gotokeep.com/hashtags/我要上精选
实际上网页请求返回的是json格式的数据，请求的真实地址为https://api.gotokeep.com/social/v3/hashtag/'+tags+'/timeline?lastId='+lastId+'&sort=heat
tags为过滤标签，lastId获取方式同上。注意输入的中文标签需要转换成URL能解析的格式，调用urllib.parse.quote()即可。


  [1]: http://www.gotokeep.com/explore
  [2]: http://www.gotokeep.com/hashtags/%E6%88%91%E8%A6%81%E4%B8%8A%E7%B2%BE%E9%80%89
