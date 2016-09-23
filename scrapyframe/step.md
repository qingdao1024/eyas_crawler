notice:https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html
----
初始化一个debian系统环境
安装所需要的依赖
apt-get update && apt-get install vim python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
安装scrapy
pip install Scrapy

----
初始化爬虫项目demo
scrapy startproject tutorial

初始化demo代码

执行抓取代码
scrapy crawl dmoz

root@iZ28a30i167Z:/mnt/eyas_crawler/scrapyframe# cd tutorial/
root@iZ28a30i167Z:/mnt/eyas_crawler/scrapyframe/tutorial# scrapy crawl dmoz
2016-09-22 11:46:52 [scrapy] INFO: Scrapy 1.1.2 started (bot: tutorial)
2016-09-22 11:46:52 [scrapy] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'tutorial.spiders', 'SPIDER_MODULES': ['tutorial.spiders'], 'ROBOTSTXT_OBEY': True, 'BOT_NAME': 'tutorial'}
2016-09-22 11:46:52 [scrapy] INFO: Enabled extensions:
['scrapy.extensions.logstats.LogStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.corestats.CoreStats']
2016-09-22 11:46:52 [scrapy] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2016-09-22 11:46:52 [scrapy] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2016-09-22 11:46:52 [scrapy] INFO: Enabled item pipelines:
[]
2016-09-22 11:46:52 [scrapy] INFO: Spider opened
2016-09-22 11:46:52 [scrapy] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2016-09-22 11:46:52 [scrapy] DEBUG: Telnet console listening on 127.0.0.1:6023
2016-09-22 11:46:54 [scrapy] DEBUG: Crawled (200) <GET http://www.dmoz.org/robots.txt> (referer: None)
2016-09-22 11:46:55 [scrapy] DEBUG: Crawled (200) <GET http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/> (referer: None)
2016-09-22 11:46:55 [scrapy] DEBUG: Crawled (200) <GET http://www.dmoz.org/Computers/Programming/Languages/Python/Books/> (referer: None)
2016-09-22 11:46:55 [scrapy] INFO: Closing spider (finished)


{'downloader/request_bytes': 734,
 'downloader/request_count': 3,
 'downloader/request_method_count/GET': 3,
 'downloader/response_bytes': 15997,
 'downloader/response_count': 3,
 'downloader/response_status_count/200': 3,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2016, 9, 22, 3, 46, 55, 886192),
 'log_count/DEBUG': 4,
 'log_count/INFO': 7,
 'response_received_count': 3,
 'scheduler/dequeued': 2,
 'scheduler/dequeued/memory': 2,
 'scheduler/enqueued': 2,
 'scheduler/enqueued/memory': 2,
 'start_time': datetime.datetime(2016, 9, 22, 3, 46, 52, 630427)}
2016-09-22 11:46:55 [scrapy] INFO: Spider closed (finished



----

测试Selector的使用方法，可以使用内置的scrape shell
安装python
pip install --upgrade pip
pip install jupyter

安装完成后进入项目根目录输入

scrapy shell "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"

等待解析。。。
当 提示   In [1]:  时，可以输入selector选择器命令
selector命令：
response.body
response.headers
。。

输入示例：
In [1]: response.xpath('//title')
Out[1]: [<Selector xpath='//title' data=u'<title>Open Directory - Computers: Progr'>]

In [2]: response.xpath('//title').extract()
Out[2]: [u'<title>Open Directory - Computers: Programming: Languages: Python: Books</title>']

In [3]: response.xpath('//title/text()')
Out[3]: [<Selector xpath='//title/text()' data=u'Open Directory - Computers: Programming:'>]

In [4]: response.xpath('//title/text()').extract()
Out[4]: [u'Open Directory - Computers: Programming: Languages: Python: Books']

In [5]: response.xpath('//title/text()').re('(\w+):')
Out[5]: [u'Computers', u'Programming', u'Languages', u'Python']

详情：https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html#shellselector

修改代码进行测试


----

结合使用item和selector

----

结合

import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
    ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(response.url, href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item

parse方法中进行 提取链接，通过scrapy.Request(url, callback=self.parse_dir_contents)方法进行回调解析

def parse_articles_follow_next_page(self, response):
    for article in response.xpath("//article"):
        item = ArticleItem()

        ... extract article data here

        yield item

    next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
    if next_page:
        url = response.urljoin(next_page[0].extract())
此处修改为一个迭代方法，进行对简单的分页数据进行抓取        yield scrapy.Request(url, self.parse_articles_follow_next_page






)




----
命令行工具：https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/commands.html




scrapy startproject myproject
  318  cd myproject/
  319  ls
  320  scrapy genspider -t basic wandoujia http://www.wandoujia.com/apps
命令行创建项目
