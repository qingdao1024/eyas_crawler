#!/usr/bin/python2.7
#-*-coding:utf-8-*-2
# 第一行 为了linux 环境下 设置默认解析器
# 第二行设置编码格式 可以中文注释和中文输入输出
import urllib2,cookielib
import bs4
import re
import time
import MySQLdb
# 导入必要包

#time.sleep(2)
from bs4 import BeautifulSoup

ISOTIMEFORMAT='%Y-%m-%d %X'
# 初始化mysql
def premysql():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='secret',db='mytest',charset='utf8')
	return conn

#添加扫描路径 - 时间点之后 不存在即添加
def addurl(url, limittime = '2016-08-15 00:00:00'):
	conn = premysql()
	cursor = conn.cursor()
	cursor.execute ("select count(1) from urls where url='"+url+"' and create_time > '"+limittime+"'")
	row = cursor.fetchone ()
	if row[0]==0:
		now = time.strftime(ISOTIMEFORMAT, time.localtime())
		sql = "INSERT INTO `mytest`.`urls` (`url`, `status`, `create_time`, `update_time`) VALUES ('"+url+"', '0', '"+now+"', '"+now+"');"
		# print(sql)
		print('add-'+url)
		cursor.execute (sql)
		conn.commit()
	cursor.close()
	conn.close()
	return True

#修改链接状态
def updatestatus(url, limittime = '2016-08-15 00:00:00'):
	conn = premysql()
	cursor = conn.cursor()
	#UPDATE `mytest`.`urls` SET `id`='1', `url`='http://www.wandoujia.com/apps', `status`='0', `create_time`='2016-08-15 05:55:57', `update_time`='2016-08-15 05:55:57' WHERE (`id`='1');

	now = time.strftime(ISOTIMEFORMAT, time.localtime())
	sql = "UPDATE `mytest`.`urls` SET `status`='1' WHERE `url`='"+url+"' and create_time > '"+limittime+"'"
	# print(sql)
	cursor.execute (sql)
	conn.commit()
	
	cursor.close()
	conn.close()
	return True

# 获取时间点之后 可抓取的路径
def geturl(limittime = '2016-08-15 00:00:00'):
	conn = premysql()
	cursor = conn.cursor()
	cursor.execute ("select url from urls where status = 0 and create_time > '"+limittime+"' limit 1;")
	row = cursor.fetchone ()
	if row!=None:
		result = row[0]
	else:
		result = ''
	#print(result)
	cursor.close()
	conn.close()
	return result

#请求页面路径-解析页面存在的路径
def requesthtml(url,limittime):
	#print('url='+url)
	response = urllib2.urlopen(url)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf8')
	nodes = soup.find_all('a',href=re.compile(r'http://www.wandoujia.com/'))
	#nodes = soup.find_all('a',href=re.compile(r'http://www.wandoujia.com/category/[0-9]{3}.*'))
	for node in nodes:
		
		nodeurl = node['href']
	#	print node.name,node['href'],node.get_text()
		text = node.get_text().strip()
		#print text
	
		#判断是否是下载链接 http://www.wandoujia.com/apps/com.huizhuang.hz/binding
		m = re.match(r'^http://www.wandoujia.com/apps/.*/binding$',nodeurl)
		if m:
			print 'download-',text,nodeurl
			continue
		
		#print nodeurl
		addurl(nodeurl,limittime) 

def start(limittime = '2016-08-15 00:00:00'):
	print('---start---',time.strftime(ISOTIMEFORMAT, time.localtime()))
	url = 'http://www.wandoujia.com/apps'
	addurl(url,limittime)
	url = geturl()
	print(url)
	while(url != ''):
		time.sleep(1) # 延时1秒
		requesthtml(url,limittime)# 请求页面，解析链接、维护后续爬虫链接
		updatestatus(url,limittime)
		url = geturl()
		
		
	print('---end---',time.strftime(ISOTIMEFORMAT, time.localtime()))
	
limittime = '2016-08-15 00:00:00'
start(limittime)







