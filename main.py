#!/usr/bin/env python
# -*- coding: utf-8 -*-
import helper
import re, os, json
from pyquery import PyQuery

goodsArr = []

def fetchGoods(url, id, category):
	global goodsArr
	pq = helper.get(url)
	name = pq('.blpt').text()
	price = pq('.blpj').text()
	shelledTotal = pq('.blsale').text()
	leftTotal = pq('.option > span').text()

	# print(name, price, shelledTotal, leftTotal)
	goodsArr.append({
		'name': name,
		'price': price,
		'shelledTotal': shelledTotal,
		'leftTotal': leftTotal,
		'category': category
	})
	csv = 'name,price,shelledTotal,leftTotal\n'
	for goods in goodsArr:
		csv += '%s,%s,%s,%s,%s,%s\n' % (id, goods.get('name'), goods.get('price'), goods.get('shelledTotal'), goods.get('leftTotal'), category)
	f = open('result%s.csv' % helper.today(), 'wb')
	f.write(csv.decode('GB18030', 'ignore').encode('utf-8'))
	f.close()

def fetchCategory(url, category):
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
				fetchGoods('http://m.ifitbox.com/%s' % href, id, category)
			if len(aArr) < 10:
				break
			page += 1
		else:
			break

if __name__ == '__main__':
	f = open('result%s.csv' % helper.today(), 'rb')
	csv = f.read()
	f.close()

	csvRowArr = csv.split('\n')
	for csvRow in csvRowArr:
		csvData = csvRow.split(',')
		goodsArr.append({
			'id': csvData[0],
			'name': csvData[1],
			'price': csvData[2],
			'shelledTotal': csvData[3],
			'leftTotal': csvData[4],
			'category': csvData[5]
		})
	pq = helper.get('http://m.ifitbox.com/cate_all.php')
	for a in pq('.blhllc > a'):
		href = a.get('href')
		if href.startswith('category'):
			fetchCategory('http://m.ifitbox.com/%s' % href, a.text)
	
	# fetchGoods('http://m.ifitbox.com/goods-670.html', '')