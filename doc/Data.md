#数据存储

##存储目标

* 保存每次抓取爬虫使用的请求头
* 保存每次抓取后目标服务器返回的响应头
* 保存每次抓取后目标服务器页面的快照
* 保存页面更新的频率
* 保存抓取任务的ID
* 保存抓取任务的调度频率
* 保存抓取时候使用的IP地址

##元数据
* 抓取任务的ID
* 抓取任务的频率
* 页面更新的频率

##快照
* 抓取时的IP地址
* 抓取时的请求头
* 服务器的响应头
* 服务器的页面快照

##ID设计

###HASH的冲突概率
[Birthday Attack](https://en.wikipedia.org/wiki/Birthday_attack)


###更新频率ID
	SHA512(Domain) + SHA512(URL) + Collision

Collision一般情况下为0，除非出现了SHA512(Domain) + SHA512(URL)完全一致的情况

###任务ID
	SHA512(Domain) + SHA512(URL) + timestamp

如此设置任务ID后，可以根据SHA512(Domain)将任务进行分区，将相同域名的任务尽可能的分配给一个爬虫来进行抓取。使用SHA512(URL) ＋ timestamp是用来降低任务冲突的概率，以及同一个URL再次被抓取的时候ID会不同。	
快照直接使用该ID作为存储ID。

##存储选择

###元数据
MySQL／PostgreSQL

###快照
CouchDB/MongoDB



