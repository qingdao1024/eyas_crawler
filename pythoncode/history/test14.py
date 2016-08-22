#!/usr/bin/python2.7
#-*-coding:utf-8-*-2
# 第一行 为了linux 环境下 设置默认解析器
# 第二行设置编码格式 可以中文注释和中文输入输出
import urllib2,cookielib
import bs4
import re
import time
import MySQLdb
import sys
import os
# 导入必要包

#time.sleep(2)
from bs4 import BeautifulSoup
# 处理 str.find('中文')报错的问题
reload(sys)
sys.setdefaultencoding('utf8')

ISOTIMEFORMAT='%Y-%m-%d %X'
# 初始化mysql
def premysql():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='secret',db='mytest',charset='utf8')
	return conn

#添加扫描路径 - 时间点之后 不存在即添加
def addurl(url, limittime = '2016-08-15 00:00:00'):
#	print 'addurl:',url
	#print url
	conn = premysql()
	cursor = conn.cursor()
	try:
		cursor.execute ("select count(1) from urls where url='"+url+"' and create_time > '"+limittime+"'")
		row = cursor.fetchone ()
		if row[0]==0:
			now = time.strftime(ISOTIMEFORMAT, time.localtime())
			sql = "INSERT INTO `mytest`.`urls` (`url`, `status`, `create_time`, `update_time`) VALUES ('"+url+"', '0', '"+now+"', '"+now+"');"
	#		print(sql)
			#print('add-'+url) #
			cursor.execute (sql)
			conn.commit()
	except:
		print 'error addurl'
	finally:
		cursor.close()
		conn.close()
	return True

#修改链接状态
def updatestatus(url, limittime = '2016-08-15 00:00:00'):
	print 'updatestatus',url
	conn = premysql()
	cursor = conn.cursor()
	#UPDATE `mytest`.`urls` SET `id`='1', `url`='http://www.wandoujia.com/apps', `status`='0', `create_time`='2016-08-15 05:55:57', `update_time`='2016-08-15 05:55:57' WHERE (`id`='1');
	try:
		now = time.strftime(ISOTIMEFORMAT, time.localtime())
		sql = "UPDATE `mytest`.`urls` SET `status`='1' WHERE `url`='"+url+"' and create_time > '"+limittime+"'"
		# print(sql)
		cursor.execute (sql)
		conn.commit()
	except:
		print 'error updatestatus'
	finally:	
		cursor.close()
		conn.close()
	return True

# 获取时间点之后 可抓取的路径
def geturl(limittime = '2016-08-15 00:00:00'):
	print 'geturl'
	conn = premysql()
	cursor = conn.cursor()
	result = ''
	try:
		cursor.execute ("select url from urls where status = 0 and create_time > '"+limittime+"' limit 1;")
		row = cursor.fetchone ()
		if row!=None:
			result = row[0]
		#print(result)
	except:
		print 'error geturl'
	finally:
		cursor.close()
		conn.close()
	return result

def dealhtml(url,soup):
	print 'dealhtml:',url
	# 判断是app信息页面 http://www.wandoujia.com/apps/com.huizhuang.hz
	m = re.match(r'^http://www.wandoujia.com/apps/com.\w*[.]{1}\w*$',url)
	if m:
		print('app信息页面：'+url)
	else:
		return 0

	softunique = url.replace(r'http://www.wandoujia.com/apps/','')#软件唯一标识
	#<span class="title" itemprop="name">惠装装修</span>
	name = soup.find('span',class_="title").get_text().strip()#名称
	
	#<div class="download-wp">
	downloadlink = soup.find('div',class_="download-wp").find('a')['href']
	#print downloadlink
	# <i itemprop="interactionCount" content="UserDownloads:65947">108 万</i>
	downloadtimes = soup.find('i',itemprop="interactionCount").get_text().strip()
	if  downloadtimes.find('亿')>-1:
		downloadtimes = downloadtimes.replace('亿','').strip()
		downloadtimes = float(downloadtimes) * 100000000
	elif downloadtimes.find('万')>-1:
		downloadtimes = downloadtimes.replace('万','').strip()
		downloadtimes = float(downloadtimes) * 10000
	else:
		downloadtimes = int(downloadtimes)
	#<span class="item love">
	suporttimes = int(soup.find('span',class_="item love").find('i').get_text().strip())
	#print suporttimes
	#<a title="查看评论" class="item last comment-open" href="#comments" rel="nofollow">
	commenttimes = int(soup.find('a',class_="item last comment-open").find('i').get_text().strip())
	#print commenttimes
	#<div class="editorComment">
	#note = soup.find('div',class_="editorComment").find('div').get_text().strip()
	#<div class="desc-info">
	note = soup.find('div',class_="desc-info").find('div').get_text().strip()
	#print note
	#print note
	# <div data-length="4" class="overview" style="width:658px">
	imgsnodes = soup.find('div',class_="overview").find_all('img')
	imgs = ''
	for imgnode in imgsnodes:
		imgs = imgs+','+imgnode['src']
	#print imgs
	#  `downloadlink` varchar(300) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '下载链接',
	#<div class="change-info">
	updatenote=''
	try:
		updatenote = soup.find('div',class_="change-info").find('div').get_text().strip()
	except:
		updatenote=''
	#print updatenote
	#<ul class="old-version-list">
	oldversions = soup.find('ul',class_="old-version-list").find_all('li')
	oldversion = ''
	olddownload = ''
	for version in oldversions:
		oldversion= oldversion + ',' + version.find('span').get_text().strip()
		olddownload = olddownload + ',' + version.find('a')['href']
	#print oldversion
	#print olddownload
	
	#<div class="col-right">
	colright =  soup.find('div',class_="col-right").find_all('div')
	
	info = colright[0].find('dl')
	#print info.contents[3].get_text().strip()
	
	#for tmp in range(0,28):
	#	print('i=',str(tmp),info.contents[tmp])
		
	version = info.contents[19].get_text().strip()
	#print version
	size = info.contents[3].get_text().strip()
	#print size
	categorynos = ''
	tag = ''
	for tmp in info.contents[7].find_all('a'):
		categorynos = categorynos+ ','+tmp['href'].split('?')[0].replace(r'http://www.wandoujia.com/category/','')
		tag = tag + ',' + tmp.get_text().strip()
	#print categorynos
	#print tag
	updatetimes = info.contents[15].get_text().strip()
	request = info.contents[23].get_text().strip()
	#print updatetimes
	#print request
	#request = info.contents[23].contents[0]
	
	createfrom = info.contents[27].get_text().strip()
	#print createfrom
	#<ul class="clearfix relative-download">
	relates = soup.find('ul',class_="clearfix relative-download")
	
	#print relate.find_all('a',data-track="detail-click-relateApp")
	relates = relates.find_all('a',href=re.compile(r'http://www.wandoujia.com/apps/com.'))
	i=1
	recommends = ''
	for relate in relates:
		if i% 2 ==0:
			recommends = recommends + ',' + relate['href']
		i=i+1
	#print recommends
	
	erweimatupian = soup.find('div',class_="qr-info").find('img')['src']
	#print erweimatupian
	
	conn = premysql()
	cursor = conn.cursor()
	try:
		cursor.execute ("select count(1) from `mytest`.`softs` where softunique='"+softunique+"' and version = '"+version+"'")
		row = cursor.fetchone ()
		if row[0]==0:
			now = time.strftime(ISOTIMEFORMAT, time.localtime())
			sql = "INSERT INTO `mytest`.`softs` ( `softunique`,`version`,`created_at`) VALUES ( '"+softunique+"','"+version+"','"+now+"');"
			cursor.execute (sql)
			conn.commit()
			#由于sql 太长 报需要用到buffer的问题 故拆开一个字段一个字段修改
			cursor.execute ("select id from `mytest`.`softs` where softunique='"+softunique+"' and version = '"+version+"'")
			row = cursor.fetchone ()
			id=row[0]
			
			sql = "UPDATE `mytest`.`softs` SET  `note`='"+note+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `imgs`='"+imgs+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `downloadlink`='"+downloadlink+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `updatenote`='"+updatenote+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `size`='"+size+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `categorynos`='"+categorynos+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `tag`='"+tag+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `updatetimes`='"+updatetimes+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `request`='"+request+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `createfrom`='"+createfrom+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `erweimatupian`='"+erweimatupian+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `recommends`='"+recommends+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `oldversion`='"+oldversion+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `olddownload`='"+olddownload+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `name`='"+name+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `downloadtimes`="+str(downloadtimes)+" WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `suporttimes`='"+str(suporttimes)+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			sql = "UPDATE `mytest`.`softs` SET  `commenttimes`='"+str(commenttimes)+"' WHERE id="+str(id)+";"
			cursor.execute (sql)
			conn.commit()
	except:
		print 'error insert softs'
	finally:
		cursor.close()
		conn.close()
	
	return True
	

#请求页面路径-解析页面存在的路径
def requesthtml(url,limittime):
	print 'requesthtml:',url
	m = re.match(r'^http://www.wandoujia.com/apps/.*/binding?.*$',url)
	if m:
		return 0
	
	try:
		response = urllib2.urlopen(url,data=None, timeout=5)
	except urllib2.URLError, e:
	  #print e.reason
	  return 0
	html_doc = response.read()
	soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf8')
	
	#处理链接标签
	nodes = soup.find_all('a',href=re.compile(r'^http://www.wandoujia.com/'))
	#nodes = soup.find_all('a',href=re.compile(r'http://www.wandoujia.com/category/[0-9]{3}.*'))
	for node in nodes:
		#print node
		nodeurl = node['href']
	#	print node.name,node['href'],node.get_text()
		text = node.get_text().strip()
		#print text
	
		# 判断是否是下载链接 http://www.wandoujia.com/apps/com.huizhuang.hz/binding
		m = re.match(r'^http://www.wandoujia.com/apps/.*/binding$',nodeurl)
		if m:
			#print 'download-',text,nodeurl
			continue		
		#print nodeurl
		addurl(nodeurl,limittime)
	try:
		dealhtml(url,soup)
	except:
		print 'error dealhtml'
	# 判断是app信息页面 http://www.wandoujia.com/apps/com.huizhuang.hz
	#m = re.match(r'^http://www.wandoujia.com/apps/com.\w*[.]{1}\w*$',url)
	#if m:
			
			
		# 页面数据维护
		#名称<span class="title" itemprop="name">惠装装修</span>

def start(limittime = '2016-08-15 00:00:00'):
	print('---start---'+time.strftime(ISOTIMEFORMAT, time.localtime()))
	url = 'http://www.wandoujia.com/apps'
	addurl(url,limittime)
	url = geturl()
	
	while(url != ''):
		filename = r'/vagrant_data/break.flag'
		if os.path.exists(filename):
			print '进入3秒等待，可执行终止命令'
			print r'/n'
			time.sleep(3) # 延时1秒
			break
		else:
			print(time.strftime(ISOTIMEFORMAT, time.localtime())+' next:'+url)
			time.sleep(1) # 延时1秒
		try:
			requesthtml(url,limittime)# 请求页面，解析链接、维护后续爬虫链接
		except:
			print 'error',url
		updatestatus(url,limittime)
		url = geturl()
		#break;# 测试的时候只运行一次用
		
		
	print('---end---',time.strftime(ISOTIMEFORMAT, time.localtime()))
	
limittime = '2016-08-15 00:00:00'
start(limittime)

#requesthtml(r'http://www.wandoujia.com/apps/com.soufun.app',limittime)
	







