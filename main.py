#!/usr/bin/env python
# -*- coding: utf-8 -*-
import helper
import re, os, json, time
from pyquery import PyQuery

goodsArr = []

def fetchGoods(url, id, category, nowTime):
	pattern = re.compile('\d+')
	global goodsArr
	pq = helper.get(url)
	name = pq('.blpt').text()
	price = pq('.blpj').text()
	price = price.replace('¥', '').strip()
	shelledTotal = pq('.blsale').text()
	shelledTotal = pattern.findall(shelledTotal)[2]
	leftTotal = pq('.option > span').text()
	leftTotal = pattern.findall(leftTotal)[0]

	goodsArr.append({
		'id': id,
		'name': name,
		'price': price,
		'shelledTotal': shelledTotal,
		'leftTotal': leftTotal,
		'category': category
	})
	csv = 'id,name,price,shelledTotal,leftTotal,category\n'
	for goods in goodsArr:
		csv += '%s,%s,%s,%s,%s,%s\n' % (goods.get('id'), goods.get('name'), goods.get('price'), goods.get('shelledTotal'), goods.get('leftTotal'), goods.get('category'))
	f = open('result%s.csv' % nowTime, 'wb')
	f.write(csv.encode('utf-8'))
	f.close()

def fetchCategory(url, category, nowTime):
	pq = helper.get(url)
	id = pq('#c_id').attr('value')

	page = 1
	while True:
		jsonText = helper.get('http://m.ifitbox.com/list.php?action=get_goods&page=%d&id=%s' % (page, id), returnType = 1)
		jsonData = json.loads(jsonText)
		if jsonData.get('error') == 0:
			pq = PyQuery(jsonData.get('content'))
			aArr = pq('li.new-mu_l2 > a')
			for a in aArr:
				href = a.get('href')
				# goods-234.html
				id = href.split('-')[1].split('.')[0]
				fetchGoods('http://m.ifitbox.com/%s' % href, id, category, nowTime)
			if len(aArr) < 10:
				break
			page += 1
		else:
			break

if __name__ == '__main__':
	# csvPath = os.path.join('.', 'result%s.csv' % helper.today())
	# if os.path.exists(csvPath):
	# 	f = open(csvPath, 'r')
	# 	csv = f.read()
	# 	f.close()
	# 	if csv != '':
	# 		csvRowArr = csv.split('\n')
	# 		isFirst = True
	# 		for csvRow in csvRowArr:
	# 			if isFirst:
	# 				isFirst = False
	# 				continue
	# 			csvData = csvRow.split(',')
	# 			goodsArr.append({
	# 				'id': csvData[0],
	# 				'name': csvData[1],
	# 				'price': csvData[2],
	# 				'shelledTotal': csvData[3],
	# 				'leftTotal': csvData[4],
	# 				'category': csvData[5]
	# 			})
	
	# 每一秒判断一下当前时间，如果是整点的话，就开始爬一次数据
	isJustBegin = True
	while True:
		nowTime = helper.timeStr()
		print('当前时间: %s' % nowTime)
		timeArr = nowTime.split(':')
		if isJustBegin or timeArr[1] == timeArr[2] == '00':
			print('刚启动爬虫，那么让小爬虫开始工作吧( •̀ ω •́ )y' if isJustBegin else '整点到了，开始爬数据咯( •̀ ω •́ )y')
			isJustBegin = False
			nowTime = helper.now().replace(':', '-')
			pq = helper.get('http://m.ifitbox.com/cate_all.php')
			for a in pq('.blhllc > a'):
				href = a.get('href')
				if href.startswith('category'):
					fetchCategory('http://m.ifitbox.com/%s' % href, a.text, nowTime)
		else:
			# 不是整点，那就等待一秒
			time.sleep(1)
	
	# fetchGoods('http://m.ifitbox.com/goods-670.html', '', '')